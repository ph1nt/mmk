import array
import time
import struct
import microcontroller
from .action_code import *
from battery import battery_level
from hid import HID
from matrix import Matrix


class Device:
    def __init__(self, kbd):
        self.kbd = kbd
        self.backlight = kbd.backlight
        self.send_consumer = kbd.send_consumer
        self.wait = kbd.matrix.wait
        self.scan = kbd.matrix.scan
        self.suspend = kbd.matrix.suspend

    def send(self, *names):
        keycodes = map(get_action_code, names)
        self.kbd.send(*keycodes)

    def press(self, *names):
        keycodes = map(get_action_code, names)
        self.kbd.press(*keycodes)

    def release(self, *names):
        keycodes = map(get_action_code, names)
        self.kbd.release(*keycodes)


class Keyboard:
    def __init__(self, keymap=(), verbose=True):
        self.keymap = keymap
        self.verbose = verbose
        self.profiles = {}
        self.pairs = ()
        self.pairs_handler = do_nothing
        self.pair_keys = set()
        self.macro_handler = do_nothing
        self.layer_mask = 1
        self.matrix = Matrix()
        self.backlight = Backlight()
        self.uid = microcontroller.cpu.uid * 2
        self.usb_status = 0
        self.tap_delay = 500
        self.fast_type_thresh = 200
        self.pair_delay = 10
        self.adv_timeout = None
        size = 4 + self.matrix.keys
        self.data = array.array("L", microcontroller.nvm[: size * 4])
        if self.data[0] != 0x424B5950:
            self.data[0] = 0x424B5950
            self.data[1] = 1
            for i in range(4, size):
                self.data[i] = 0
        self.ble_id = self.data[1]
        self.heatmap = memoryview(self.data)[4:]
        self.battery.level = battery_level()
        self.advertisement = ProvideServicesAdvertisement(ble_hid, self.battery)
        self.advertisement.appearance = 961
        self.ble = BLERadio()
        self.set_bt_id(self.ble_id)
        self.ble_hid = HID(ble_hid.devices)

    def on_device_changed(self, name):
        print("change to {}".format(name))
        if name in self.actionmaps:
            self.actionmap = self.actionmaps[name]
        else:
            self.actionmap = self.default_actionmap
        # reset `layer_mask` when keymap is changed
        self.layer_mask = 1

    def check(self):
        if self.adv_timeout:
            if self.ble.connected:
                self.adv_timeout = 0
                self.backlight.set_bt_led(None)
            elif time.time() > self.adv_timeout:
                self.stop_advertising()
            self.on_device_changed("BT{}".format(self.ble_id))
            if not self.ble.connected and not self.ble._adapter.advertising:
                self.start_advertising()
        elif self.ble.connected:
            self.backlight.set_hid_leds(self.ble_hid.leds)
        # update battery level
        if time.time() > self.battery_update_time:
            self.battery_update_time = time.time() + 3600
            self.battery.level = battery_level()

    def setup(self):
        def convert(a): return array.array("H", (get_action_code(k) for k in a))
        self.default_actionmap = tuple(convert(layer) for layer in self.keymap)
        self.actionmap = self.default_actionmap
        self.actionmaps = {}
        for key in self.profiles:
            self.actionmaps[key] = tuple(
                convert(layer) for layer in self.profiles[key]
            )
        for pair in self.pairs:
            for key in pair:
                self.pair_keys.add(key)

    def start_advertising(self):
        self.ble.start_advertising(self.advertisement)
        self.backlight.set_bt_led(self.ble_id)
        self.adv_timeout = time.time() + 60

    def stop_advertising(self):
        try:
            self.backlight.set_bt_led(None)
            self.adv_timeout = 0
            self.ble.stop_advertising()
        except Exception as e:
            print(e)

    def get_key_sequence_info(self, start, end):
        """Get the info from a sequence of key events"""
        matrix = self.matrix
        event = matrix.view(start - 1)
        key = event & 0x7F
        desc = key_name(key)
        if event < 0x80:
            desc += " \\ "
            t0 = matrix.get_keydown_time(key)
        else:
            desc += " / "
            t0 = matrix.get_keyup_time(key)
        t = []
        for i in range(start, end):
            event = matrix.view(i)
            key = event & 0x7F
            desc += key_name(key)
            if event < 0x80:
                desc += " \\ "
                t1 = matrix.get_keydown_time(key)
            else:
                desc += " / "
                t1 = matrix.get_keyup_time(key)
            dt = matrix.ms(t1 - t0)
            t0 = t1
            t.append(dt)
        return desc, t

    def is_tapping_key(self, key):
        """Check if the key is tapped (press & release quickly)"""
        matrix = self.matrix
        n = len(matrix)
        if n == 0:
            n = matrix.wait(
                self.tap_delay - matrix.ms(matrix.time() - matrix.get_keydown_time(key))
            )
        target = key | 0x80
        if n >= 1:
            new_key = matrix.view(0)
            if new_key == target:
                return True
            if new_key >= 0x80:
                # Fast Typing - B is a tap-key
                #   A???      B???      A???      B???
                # --+-------+-------+-------+------> t
                #           |  dt1  |
                #         dt1 < tap_delay
                if self.verbose:
                    desc, t = self.get_key_sequence_info(-1, n)
                    print(desc)
                    print(t)
                return True
            if n == 1:
                n = matrix.wait(
                    self.fast_type_thresh
                    - matrix.ms(matrix.time() - matrix.get_keydown_time(new_key))
                )
        if n < 2:
            return False
        if target == matrix.view(1):
            # Fast Typing - B is a tap-key
            #   B???      C???      B???      C???
            # --+-------+-------+-------+------> t
            #   |  dt1  |  dt2  |
            # dt1 < tap_delay && dt2 < fast_type_thresh
            if self.verbose:
                desc, t = self.get_key_sequence_info(-1, n)
                print(desc)
                print(t)
            return True
        if self.verbose:
            desc, t = self.get_key_sequence_info(-1, n)
            print(desc)
            print(t)
        return False

    def set_bt_id(self, n):
        if 0 > n or n > 9:
            n = 0
        if self.ble.connected:
            self.ble_hid.release_all()
            for c in self.ble.connections:
                c.disconnect()
        if self.ble._adapter.advertising:
            self.ble.stop_advertising()
        uid = self.uid[n: n + 6]
        uid[-1] = uid[-1] | 0xC0
        address = _bleio.Address(uid, _bleio.Address.RANDOM_STATIC)
        try:
            self.ble._adapter.address = address
            name = "PYKB {}".format(n)
            self.advertisement.complete_name = name
            self.ble.name = name
            self.ble_id = n
            if self.data[1] != n:
                self.data[1] = n
                microcontroller.nvm[:272] = struct.pack("68L", *self.data)
        except Exception as e:
            print(e)
        self.log(self.ble._adapter.address)

    def change_bt(self, n):
        changed = False
        if self.usb_status == 3:
            self.usb_status = 1
            changed = True
        if n != self.ble_id:
            changed = True
            self.set_bt_id(n)
            self.start_advertising()
        elif not self.ble.connected and not self.ble._adapter.advertising:
            self.start_advertising()
        if changed:
            self.on_device_changed("BT{}".format(n))

    def action_code(self, position):
        position = COORDS[position]
        layer_mask = self.layer_mask
        for layer in range(len(self.actionmap) - 1, -1, -1):
            if (layer_mask >> layer) & 1:
                code = self.actionmap[layer][position]
                if code == 1:  # TRANSPARENT
                    continue
                return code
        return 0

    def log(self, *args):
        if self.verbose:
            print(*args)

    def send(self, *keycodes):
        self.press(*keycodes)
        self.release(*keycodes)

    def press(self, *keycodes):
        try:
            if self.usb_status == 0x3 and usb_is_connected():
                self.usb_hid.press(*keycodes)
            elif self.ble.connected:
                self.ble_hid.press(*keycodes)
            elif not self.ble._adapter.advertising:
                self.start_advertising()
        except Exception as e:
            print(e)

    def release(self, *keycodes):
        try:
            if self.usb_status == 0x3 and usb_is_connected():
                self.usb_hid.release(*keycodes)
            elif self.ble.connected:
                self.ble_hid.release(*keycodes)
        except Exception as e:
            print(e)

    def send_consumer(self, keycode):
        try:
            if self.usb_status == 0x3 and usb_is_connected():
                self.usb_hid.send_consumer(keycode)
            elif self.ble.connected:
                self.ble_hid.send_consumer(keycode)
        except Exception as e:
            print(e)

    def get(self):
        event = self.matrix.get()
        key = event & 0x7F
        pressed = event < 0x80
        if pressed:
            self.heatmap[key] += 1
        self.backlight.handle_key(key, pressed)
        return event

    def run(self):
        self.setup()
        log = self.log
        matrix = self.matrix
        dev = Device(self)
        keys = [0] * matrix.keys
        ms = matrix.ms
        last_time = 0
        mouse_action = 0
        mouse_time = 0
        while True:
            t = 20 if self.backlight.check() or mouse_action else 1000
            n = matrix.wait(t)
            self.check()
            if self.pair_keys:
                # detecting pair keys
                if n == 1:
                    key = matrix.view(0)
                    if key < 0x80 and key in self.pair_keys:
                        n = matrix.wait(
                            self.pair_delay
                            - ms(matrix.time() - matrix.get_keydown_time(key))
                        )
                if n >= 2:
                    pair = {matrix.view(0), matrix.view(1)}
                    if pair in self.pairs:
                        pair_index = self.pairs.index(pair)
                        key1 = self.get()
                        key2 = self.get()
                        dt = ms(
                            matrix.get_keydown_time(key2)
                            - matrix.get_keydown_time(key1)
                        )
                        log("pair keys {} {}, dt = {}".format(pair_index, pair, dt))
                        try:
                            self.pairs_handler(dev, pair_index)
                        except Exception as e:
                            print(e)
            while len(matrix):
                event = self.get()
                key = event & 0x7F
                if event & 0x80 == 0:
                    action_code = self.action_code(key)
                    keys[key] = action_code
                    if action_code < 0xFF:
                        self.press(action_code)
                    else:
                        kind = action_code >> 12
                        if kind < ACT_MODS_TAP:
                            # MODS
                            mods = (action_code >> 8) & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            keycodes.append(action_code & 0xFF)
                            self.press(*keycodes)
                        elif kind < ACT_USAGE:
                            # MODS_TAP
                            if self.is_tapping_key(key):
                                log("TAP")
                                keycode = action_code & 0xFF
                                keys[key] = keycode
                                self.press(keycode)
                            else:
                                mods = (action_code >> 8) & 0x1F
                                keycodes = mods_to_keycodes(mods)
                                self.press(*keycodes)
                        elif kind == ACT_USAGE:
                            if action_code & 0x400:
                                self.send_consumer(action_code & 0x3FF)
                        elif kind == ACT_MOUSEKEY:
                            if action_code & 0xF00 == 0:
                                self.press_mouse(action_code & 0xF)
                            else:
                                mouse_action = (action_code >> 8) & 0xF
                                mouse_time = time.monotonic_ns()
                        elif kind == ACT_LAYER_TAP or kind == ACT_LAYER_TAP_EXT:
                            layer = (action_code >> 8) & 0x1F
                            mask = 1 << layer
                            if action_code & 0xE0 == 0xC0:
                                log("LAYER_MODS")
                                mods = action_code & 0x1F
                                keycodes = mods_to_keycodes(mods)
                                self.press(*keycodes)
                                self.layer_mask |= mask
                            elif self.is_tapping_key(key):
                                log("TAP")
                                keycode = action_code & 0xFF
                                if keycode == OP_TAP_TOGGLE:
                                    log("TOGGLE {}".format(layer))
                                    self.layer_mask = (self.layer_mask & ~mask) | (
                                        mask & ~self.layer_mask
                                    )
                                    keys[key] = 0
                                else:
                                    keys[key] = keycode
                                    self.press(keycode)
                            else:
                                self.layer_mask |= mask
                            log("layer_mask = {}".format(self.layer_mask))
                        elif kind == ACT_MACRO:
                            if callable(self.macro_handler):
                                i = action_code & 0xFFF
                                try:
                                    self.macro_handler(dev, i, True)
                                except Exception as e:
                                    print(e)
                        elif kind == ACT_BACKLIGHT:
                            if action_code == RGB_MOD:
                                self.backlight.next()
                            elif action_code == RGB_TOGGLE:
                                self.backlight.toggle()
                            elif action_code == RGB_HUE:
                                self.backlight.hue += 8
                            elif action_code == HUE_RGB:
                                self.backlight.hue -= 8
                            elif action_code == RGB_SAT:
                                self.backlight.sat += 8
                            elif action_code == SAT_RGB:
                                self.backlight.sat -= 8
                            elif action_code == RGB_VAL:
                                self.backlight.val += 8
                            elif action_code == VAL_RGB:
                                self.backlight.val -= 8
                        elif kind == ACT_COMMAND:
                            if action_code == BOOTLOADER:
                                microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
                                microcontroller.reset()
                            elif action_code == SUSPEND:
                                matrix.suspend()
                            elif action_code == SHUTDOWN:
                                microcontroller.reset()
                            elif action_code == HEATMAP:
                                microcontroller.nvm[:272] = struct.pack(
                                    "68L", *self.data
                                )
                                if usb_is_connected():
                                    microcontroller.reset()
                            elif action_code == USB_TOGGLE:
                                self.toggle_usb()
                            elif action_code == BT_TOGGLE:
                                self.toggle_bt()
                            elif BT(0) <= action_code and action_code <= BT(9):
                                i = action_code - BT(0)
                                log("switch to bt {}".format(i))
                                self.change_bt(i)
                    if self.verbose:
                        keydown_time = matrix.get_keydown_time(key)
                        dt = ms(matrix.time() - keydown_time)
                        dt2 = ms(keydown_time - last_time)
                        last_time = keydown_time
                        print(
                            "{} {} \\ {} latency {} | {}".format(
                                key, key_name(key), hex(action_code), dt, dt2
                            )
                        )
                else:
                    action_code = keys[key]
                    if action_code < 0xFF:
                        self.release(action_code)
                    else:
                        kind = action_code >> 12
                        if kind < ACT_MODS_TAP:
                            # MODS
                            mods = (action_code >> 8) & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            keycodes.append(action_code & 0xFF)
                            self.release(*keycodes)
                        elif kind < ACT_USAGE:
                            # MODS_TAP
                            mods = (action_code >> 8) & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            self.release(*keycodes)
                        elif kind == ACT_USAGE:
                            if action_code & 0x400:
                                self.send_consumer(0)
                        elif kind == ACT_MOUSEKEY:
                            if action_code & 0xF00 == 0:
                                self.release_mouse(action_code & 0xF)
                            elif (action_code >> 8) & 0xF == mouse_action:
                                mouse_action = 0
                                self.move_mouse(0, 0, 0)
                        elif kind == ACT_LAYER_TAP or kind == ACT_LAYER_TAP_EXT:
                            layer = (action_code >> 8) & 0x1F
                            keycode = action_code & 0xFF
                            if keycode & 0xE0 == 0xC0:
                                log("LAYER_MODS")
                                mods = keycode & 0x1F
                                keycodes = mods_to_keycodes(mods)
                                self.release(*keycodes)
                            self.layer_mask &= ~(1 << layer)
                            log("layer_mask = {}".format(self.layer_mask))
                        elif kind == ACT_MACRO:
                            i = action_code & 0xFFF
                            try:
                                self.macro_handler(dev, i, False)
                            except Exception as e:
                                print(e)
                    if self.verbose:
                        keyup_time = matrix.get_keyup_time(key)
                        dt = ms(matrix.time() - keyup_time)
                        dt2 = ms(keyup_time - last_time)
                        last_time = keyup_time
                        print(
                            "{} {} / {} latency {} | {}".format(
                                key, key_name(key), hex(action_code), dt, dt2
                            )
                        )
            if mouse_action:
                x, y, wheel = MS_MOVEMENT[mouse_action]
                dt = 1 + (time.monotonic_ns() - mouse_time) // 8000000
                mouse_time = time.monotonic_ns()
                self.move_mouse(x * dt, y * dt, wheel * dt)


keyboard = Keyboard()
___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2D = LAYER_TAP(2, D)
L3B = LAYER_TAP(3, B)
LSFT4 = LAYER_MODS(4, MODS(LSHIFT))
RSFT4 = LAYER_MODS(4, MODS(RSHIFT))
L5S = LAYER_TAP(5, S)
# Semicolon & Ctrl
SCC = MODS_TAP(MODS(RCTRL), ';')
SINS = MODS_KEY(MODS(SHIFT), INSERT)
keyboard.keymap = (
    # layer 0
    (
        ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        CAPS,  A,   S, L2D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
        LSFT4, Z,   X,   C,   V, L3B,   N,   M, ',', '.', '/',         RSFT4,
        LCTRL, LGUI, LALT,          SPACE,            RALT, MENU,  L1, RCTRL
    ),
    # layer 1
    (
        '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___, SUSPEND, ___, ___, ___,
        ___, LEFT, DOWN, RIGHT, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, BOOT, ___, MACRO(0), ___, ___, ___,       ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
    # layer 2
    (
        '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___, ___, ___, ___, ___, HOME, PGUP, ___, ___, SINS, AUDIO_VOL_DOWN, AUDIO_VOL_UP, AUDIO_MUTE,
        ___, ___, ___, ___, ___, ___, LEFT, DOWN, UP, RIGHT, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, PGDN, END, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
    # layer 3
    (
        BT_TOGGLE, BT1, BT2, BT3, BT4, BT5, BT6, BT7, BT8, BT9, BT0, ___, ___, ___,
        RGB_MOD, ___, ___, ___, ___, ___, ___, USB_TOGGLE, ___, ___, ___, ___, ___, ___,
        RGB_TOGGLE, HUE_RGB, RGB_HUE, SAT_RGB, RGB_SAT, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, VAL_RGB, RGB_VAL, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
    # layer 4
    (
        '`', ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___,   D, ___, ___, ___, ___, ___, ___, ';', ___,      ___,
        ___, ___, ___, ___, ___,   B, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
    # layer 5
    (
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, MS_W_UP, MS_UL, MS_UP, MS_UR, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, MS_BTN1, MS_LT, MS_DN, MS_RT, MS_BTN2, ___,      ___,
        ___, ___, ___, ___, ___, ___, MS_W_DN, MS_DL, MS_DN, MS_DR, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
)
# Use different keymaps on different connections
# Valid keys are "USB" and "BT0"-"BT9"
# Connection not in this map will use default keymap defined above.
keyboard.profiles = {
    # For example, BT8 is connected to a Mac
    "BT8": (
        # layer 0
        (
            ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
            TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
            CAPS,  A,   S,   D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
            LSHIFT, Z,   X,   C,   V,   B,   N,   M, ',', '.', '/',        RSHIFT,
            LCTRL, LALT, LGUI,          SPACE,            MENU, RALT,  L1, RCTRL
        ),
        # layer 1
        (
            '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
            ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___, SUSPEND, ___, ___, ___,
            ___, LEFT, DOWN, RIGHT, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
            ___, ___, ___, ___, ___, BOOT, ___, MACRO(1), ___, ___, ___,       ___,
            ___, ___, ___,                ___,               ___, ___, ___,  ___
        ),
    )
}


def macro_handler(dev, n, is_down):
    if is_down:
        dev.send_text('You pressed macro #{}\n'.format(n))
    else:
        dev.send_text('You released macro #{}\n'.format(n))


def pairs_handler(dev, n):
    dev.send_text('You just triggered pair keys #{}\n'.format(n))


keyboard.macro_handler = macro_handler
keyboard.pairs_handler = pairs_handler
# ESC(0)    1(1)   2(2)   3(3)   4(4)   5(5)   6(6)   7(7)   8(8)   9(9)   0(10)  -(11)  =(12)  BACKSPACE(13)
# TAB(27)   Q(26)  W(25)  E(24)  R(23)  T(22)  Y(21)  U(20)  I(19)  O(18)  P(17)  [(16)  ](15)   \(14)
# CAPS(28)  A(29)  S(30)  D(31)  F(32)  G(33)  H(34)  J(35)  K(36)  L(37)  ;(38)  "(39)      ENTER(40)
# LSHIFT(52) Z(51)  X(50)  C(49)  V(48)  B(47)  N(46)  M(45)  ,(44)  .(43)  /(42)            RSHIFT(41)
# LCTRL(53)  LGUI(54)  LALT(55)               SPACE(56)          RALT(57)  MENU(58)  Fn(59)  RCTRL(60)
# Pairs: J & K, U & I
keyboard.pairs = [{35, 36}, {20, 19}]
# keyboard.verbose = False
keyboard.run()
