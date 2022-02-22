
''' Keyboard/Keypad Page(0x07) '''

# 16bit code: action_kind(4bit) + action_parameter(12bit)

# Key Actions(00xx)
# -----------------
# ACT_MODS(000r):
# 000r | 0000 | 0000 0000    No action code
# 000r | 0000 | 0000 0001    Transparent code
# 000r | 0000 | keycode     Key
# 000r | mods | 0000 0000    Modifiers
# 000r | mods | keycode     Modifiers+Key(Modified key)
#   r: Left/Right flag(Left: 0, Right: 1)

# ACT_MODS_TAP(001r):
# 001r | mods | keycode     Modifiers with Tap Key(Dual role)
# Mods:   43210
#   bit 0 ||||+- Control
#   bit 1 |||+-- Shift
#   bit 2 ||+--- Alt
#   bit 3 |+---- Gui
#   bit 4 +----- LR flag(Left: 0, Right: 1)

# Other Keys(01xx)
# ----------------
# ACT_USAGE(0100): TODO: Not needed?
# 0100 | 00 | usage(10)     System control(0x80) - General Desktop page(0x01)
# 0100 | 01 | usage(10)     Consumer control(0x01) - Consumer page(0x0C)

# ACT_LAYER_TAP(100x):
# 1llr | mods | keycode     Modifiers with Tap Key(Dual role)
#   l: layer 00-default, 01-upper, 10-lower, 11-function
##

KC_NO = 0x00
KC_ROLL_OVER = 0x01
KC_POST_FAIL = 0x02
KC_UNDEFINED = 0x03
KC_A = 0x04
KC_B = 0x05
KC_C = 0x06
KC_D = 0x07
KC_E = 0x08
KC_F = 0x09
KC_G = 0x0A
KC_H = 0x0B
KC_I = 0x0C
KC_J = 0x0D
KC_K = 0x0E
KC_L = 0x0F
KC_M = 0x10
KC_N = 0x11
KC_O = 0x12
KC_P = 0x13
KC_Q = 0x14
KC_R = 0x15
KC_S = 0x16
KC_T = 0x17
KC_U = 0x18
KC_V = 0x19
KC_W = 0x1A
KC_X = 0x1B
KC_Y = 0x1C
KC_Z = 0x1D
KC_1 = 0x1E
KC_2 = 0x1F
KC_3 = 0x20
KC_4 = 0x21
KC_5 = 0x22
KC_6 = 0x23
KC_7 = 0x24
KC_8 = 0x25
KC_9 = 0x26
KC_0 = 0x27
KC_ENTER = 0x28
KC_ESCAPE = 0x29
KC_BSPACE = 0x2A
KC_TAB = 0x2B
KC_SPACE = 0x2C
KC_MINUS = 0x2D
KC_EQUAL = 0x2E
KC_LBRACKET = 0x2F
KC_RBRACKET = 0x30
KC_BSLASH = 0x31
KC_NONUS_HASH = 0x32
KC_SCOLON = 0x33
KC_QUOTE = 0x34
KC_GRAVE = 0x35
KC_COMMA = 0x36
KC_DOT = 0x37
KC_SLASH = 0x38
KC_CAPSLOCK = 0x39
KC_F1 = 0x3A
KC_F2 = 0x3B
KC_F3 = 0x3C
KC_F4 = 0x3D
KC_F5 = 0x3E
KC_F6 = 0x3F
KC_F7 = 0x40
KC_F8 = 0x41
KC_F9 = 0x42
KC_F10 = 0x43
KC_F11 = 0x44
KC_F12 = 0x45
KC_PSCREEN = 0x46
KC_SCROLLLOCK = 0x47
KC_PAUSE = 0x48
KC_INSERT = 0x49
KC_HOME = 0x4A
KC_PGUP = 0x4B
KC_DELETE = 0x4C
KC_END = 0x4D
KC_PGDOWN = 0x4E
KC_RIGHT = 0x4F
KC_LEFT = 0x50
KC_DOWN = 0x51
KC_UP = 0x52
KC_NUMLOCK = 0x53
KC_KP_SLASH = 0x54
KC_KP_ASTERISK = 0x55
KC_KP_MINUS = 0x56
KC_KP_PLUS = 0x57
KC_KP_ENTER = 0x58
KC_KP_1 = 0x59
KC_KP_2 = 0x5A
KC_KP_3 = 0x5B
KC_KP_4 = 0x5C
KC_KP_5 = 0x5D
KC_KP_6 = 0x5E
KC_KP_7 = 0x5F
KC_KP_8 = 0x60
KC_KP_9 = 0x61
KC_KP_0 = 0x62
KC_KP_DOT = 0x63
KC_NONUS_BSLASH = 0x64
KC_APPLICATION = 0x65
KC_POWER = 0x66
KC_KP_EQUAL = 0x67
KC_F13 = 0x68
KC_F14 = 0x69
KC_F15 = 0x6A
KC_F16 = 0x6B
KC_F17 = 0x6C
KC_F18 = 0x6D
KC_F19 = 0x6E
KC_F20 = 0x6F
KC_F21 = 0x70
KC_F22 = 0x71
KC_F23 = 0x72
KC_F24 = 0x73
KC_EXECUTE = 0x74
KC_HELP = 0x75
KC_MENU = 0x76
KC_SELECT = 0x77
KC_STOP = 0x78
KC_AGAIN = 0x79
KC_UNDO = 0x7A
KC_CUT = 0x7B
KC_COPY = 0x7C
KC_PASTE = 0x7D
KC_FIND = 0x7E
KC__MUTE = 0x7F
KC__VOLUP = 0x80
KC__VOLDOWN = 0x81
KC_LOCKING_CAPS = 0x82
KC_LOCKING_NUM = 0x83
KC_LOCKING_SCROLL = 0x84
KC_KP_COMMA = 0x85
KC_KP_EQUAL_AS400 = 0x86
KC_INT1 = 0x87
KC_INT2 = 0x88
KC_INT3 = 0x89
KC_INT4 = 0x8A
KC_INT5 = 0x8B
KC_INT6 = 0x8C
KC_INT7 = 0x8D
KC_INT8 = 0x8E
KC_INT9 = 0x8F
KC_LANG1 = 0x90
KC_LANG2 = 0x91
KC_LANG3 = 0x92
KC_LANG4 = 0x93
KC_LANG5 = 0x94
KC_LANG6 = 0x95
KC_LANG7 = 0x96
KC_LANG8 = 0x97
KC_LANG9 = 0x98
KC_ALT_ERASE = 0x99
KC_SYSREQ = 0x9A
KC_CANCEL = 0x9B
KC_CLEAR = 0x9C
KC_PRIOR = 0x9D
KC_RETURN = 0x9E
KC_SEPARATOR = 0x9F
KC_OUT = 0xA0
KC_OPER = 0xA1
KC_CLEAR_AGAIN = 0xA2
KC_CRSEL = 0xA3
KC_EXSEL = 0xA4

KC_KP_00 = 0xB0
KC_KP_000 = 0xB1
KC_THOUSANDS_SEPARATOR = 0xB2
KC_DECIMAL_SEPARATOR = 0xB3
KC_CURRENCY_UNIT = 0xB4
KC_CURRENCY_SUB_UNIT = 0xB5
KC_KP_LPAREN = 0xB6
KC_KP_RPAREN = 0xB7
KC_KP_LCBRACKET = 0xB8
KC_KP_RCBRACKET = 0xB9
KC_KP_TAB = 0xBA
KC_KP_BSPACE = 0xBB
KC_KP_A = 0xBC
KC_KP_B = 0xBD
KC_KP_C = 0xBE
KC_KP_D = 0xBF
KC_KP_E = 0xC0
KC_KP_F = 0xC1
KC_KP_XOR = 0xC2
KC_KP_HAT = 0xC3
KC_KP_PERC = 0xC4
KC_KP_LT = 0xC5
KC_KP_GT = 0xC6
KC_KP_AND = 0xC7
KC_KP_LAZYAND = 0xC8
KC_KP_OR = 0xC9
KC_KP_LAZYOR = 0xCA
KC_KP_COLON = 0xCB
KC_KP_HASH = 0xCC
KC_KP_SPACE = 0xCD
KC_KP_ATMARK = 0xCE
KC_KP_EXCLAMATION = 0xCF
KC_KP_MEM_STORE = 0xD0
KC_KP_MEM_RECALL = 0xD1
KC_KP_MEM_CLEAR = 0xD2
KC_KP_MEM_ADD = 0xD3
KC_KP_MEM_SUB = 0xD4
KC_KP_MEM_MUL = 0xD5
KC_KP_MEM_DIV = 0xD6
KC_KP_PLUS_MINUS = 0xD7
KC_KP_CLEAR = 0xD8
KC_KP_CLEAR_ENTRY = 0xD9
KC_KP_BINARY = 0xDA
KC_KP_OCTAL = 0xDB
KC_KP_DECIMAL = 0xDC
KC_KP_HEXADECIMAL = 0xDD

# Modifiers
KC_LCTRL = 0xE0
KC_LSHIFT = 0xE1
KC_LALT = 0xE2
KC_LGUI = 0xE3
KC_RCTRL = 0xE4
KC_RSHIFT = 0xE5
KC_RALT = 0xE6
KC_RGUI = 0xE7

# 0xF0-0xFF are unallocated in the HID spec.
# QMK uses these for Mouse Keys - see below.

# Media and Function keys
# Generic Desktop Page(0x01)
KC_SYSTEM_POWER = 0xA5
KC_SYSTEM_SLEEP = 0xA6
KC_SYSTEM_WAKE = 0xA7

# Consumer Page(0x0C)
KC_AUDIO_MUTE = 0x0D
KC_AUDIO_VOL_UP = 0x0E
KC_AUDIO_VOL_DOWN = 0x0F
KC_MEDIA_NEXT_TRACK = 0x10
KC_MEDIA_PREV_TRACK = 0x11
KC_MEDIA_STOP = 0x12
KC_MEDIA_PLAY_PAUSE = 0x13
KC_MEDIA_SELECT = 0x14
KC_MEDIA_EJECT = 0xB0
KC_MAIL = 0xB1
KC_CALCULATOR = 0xB2
KC_MY_COMPUTER = 0xB3
KC_WWW_SEARCH = 0xB4
KC_WWW_HOME = 0xB5
KC_WWW_BACK = 0xB6
KC_WWW_FORWARD = 0xB7
KC_WWW_STOP = 0xB8
KC_WWW_REFRESH = 0xB9
KC_WWW_FAVORITES = 0xBA
KC_MEDIA_FAST_FORWARD = 0xBB
KC_MEDIA_REWIND = 0xBC
KC_BRIGHTNESS_UP = 0xBD
KC_BRIGHTNESS_DOWN = 0xBE

# Fn keys
KC_FN0 = 0xC0
KC_FN1 = 0xC1
KC_FN2 = 0xC2
KC_FN3 = 0xC3
KC_FN4 = 0xC4
KC_FN5 = 0xC5
KC_FN6 = 0xC6
KC_FN7 = 0xC7
KC_FN8 = 0xC8
KC_FN9 = 0xC9
KC_FN10 = 0xCA
KC_FN11 = 0xCB
KC_FN12 = 0xCC
KC_FN13 = 0xCD
KC_FN14 = 0xCE
KC_FN15 = 0xCF
KC_FN16 = 0xD0
KC_FN17 = 0xD1
KC_FN18 = 0xD2
KC_FN19 = 0xD3
KC_FN20 = 0xD4
KC_FN21 = 0xD5
KC_FN22 = 0xD6
KC_FN23 = 0xD7
KC_FN24 = 0xD8
KC_FN25 = 0xD9
KC_FN26 = 0xDA
KC_FN27 = 0xDB
KC_FN28 = 0xDC
KC_FN29 = 0xDD
KC_FN30 = 0xDE
KC_FN31 = 0xDF


def MOD_BIT(code): return (1 << MOD_INDEX(code))
def MOD_INDEX(code): return ((code) & 0x07)


# Short names for ease of definition of keymap
KC_TRANSPARENT = 0x01
KC_TRNS = KC_TRANSPARENT
# Punctuation
KC_EXLM = KC_KP_EXCLAMATION
KC_ENT = KC_ENTER
KC_ESC = KC_ESCAPE
KC_BSPC = KC_BSPACE
KC_SPC = KC_SPACE
KC_MINS = KC_MINUS
KC_EQL = KC_EQUAL
KC_LBRC = KC_LBRACKET
KC_RBRC = KC_RBRACKET
KC_BSLS = KC_BSLASH
KC_NUHS = KC_NONUS_HASH
KC_SCLN = KC_SCOLON
KC_QUOT = KC_QUOTE
KC_GRV = KC_GRAVE
KC_COMM = KC_COMMA
KC_SLSH = KC_SLASH
KC_NUBS = KC_NONUS_BSLASH
# Lock Keys
KC_CLCK = KC_CAPSLOCK
KC_CAPS = KC_CAPSLOCK
KC_SLCK = KC_SCROLLLOCK
KC_NLCK = KC_NUMLOCK
KC_LCAP = KC_LOCKING_CAPS
KC_LNUM = KC_LOCKING_NUM
KC_LSCR = KC_LOCKING_SCROLL
# Commands
KC_PSCR = KC_PSCREEN
KC_PAUS = KC_PAUSE
KC_BRK = KC_PAUSE
KC_INS = KC_INSERT
KC_DEL = KC_DELETE
KC_PGDN = KC_PGDOWN
KC_RGHT = KC_RIGHT
KC_APP = KC_APPLICATION
KC_EXEC = KC_EXECUTE
KC_SLCT = KC_SELECT
KC_AGIN = KC_AGAIN
KC_PSTE = KC_PASTE
KC_ERAS = KC_ALT_ERASE
KC_CLR = KC_CLEAR
# Keypad
KC_PSLS = KC_KP_SLASH
KC_PAST = KC_KP_ASTERISK
KC_PMNS = KC_KP_MINUS
KC_PPLS = KC_KP_PLUS
KC_PENT = KC_KP_ENTER
KC_P1 = KC_KP_1
KC_P2 = KC_KP_2
KC_P3 = KC_KP_3
KC_P4 = KC_KP_4
KC_P5 = KC_KP_5
KC_P6 = KC_KP_6
KC_P7 = KC_KP_7
KC_P8 = KC_KP_8
KC_P9 = KC_KP_9
KC_P0 = KC_KP_0
KC_PDOT = KC_KP_DOT
KC_PEQL = KC_KP_EQUAL
KC_PCMM = KC_KP_COMMA
# Japanese specific
KC_ZKHK = KC_GRAVE
KC_RO = KC_INT1
KC_KANA = KC_INT2
KC_JYEN = KC_INT3
KC_HENK = KC_INT4
KC_MHEN = KC_INT5
# Korean specific
KC_HAEN = KC_LANG1
KC_HANJ = KC_LANG2
# Modifiers
KC_LCTL = KC_LCTRL
KC_LSFT = KC_LSHIFT
KC_LOPT = KC_LALT
KC_LCMD = KC_LGUI
KC_LWIN = KC_LGUI
KC_RCTL = KC_RCTRL
KC_RSFT = KC_RSHIFT
KC_ALGR = KC_RALT
KC_ROPT = KC_RALT
KC_RCMD = KC_RGUI
KC_RWIN = KC_RGUI
# Generic Desktop Page(0x01)
KC_PWR = KC_SYSTEM_POWER
KC_SLEP = KC_SYSTEM_SLEEP
KC_WAKE = KC_SYSTEM_WAKE
# Consumer Page(0x0C)
KC_MUTE = KC_AUDIO_MUTE
KC_VOLU = KC_AUDIO_VOL_UP
KC_VOLD = KC_AUDIO_VOL_DOWN
KC_MNXT = KC_MEDIA_NEXT_TRACK
KC_MPRV = KC_MEDIA_PREV_TRACK
KC_MSTP = KC_MEDIA_STOP
KC_MPLY = KC_MEDIA_PLAY_PAUSE
KC_MSEL = KC_MEDIA_SELECT
KC_EJCT = KC_MEDIA_EJECT
KC_CALC = KC_CALCULATOR
KC_MYCM = KC_MY_COMPUTER
KC_WSCH = KC_WWW_SEARCH
KC_WHOM = KC_WWW_HOME
KC_WBAK = KC_WWW_BACK
KC_WFWD = KC_WWW_FORWARD
KC_WSTP = KC_WWW_STOP
KC_WREF = KC_WWW_REFRESH
KC_WFAV = KC_WWW_FAVORITES
KC_MFFD = KC_MEDIA_FAST_FORWARD
KC_MRWD = KC_MEDIA_REWIND
KC_BRIU = KC_BRIGHTNESS_UP
KC_BRID = KC_BRIGHTNESS_DOWN
# System Specific
KC_BRMU = KC_PAUSE
KC_BRMD = KC_SCROLLLOCK


def IS_ERROR(code): return (KC_ROLL_OVER <= (code) and (code) <= KC_UNDEFINED)
def IS_ANY(code): return (KC_A <= (code) and (code) <= 0xFF)
def IS_KEY(code): return (KC_A <= (code) and (code) <= KC_EXSEL)
def IS_MOD(code): return (KC_LCTRL <= (code) and (code) <= KC_RGUI)
def IS_SPECIAL(code): return (0xA5 <= (code) and (code) <= 0xDF) or (0xE8 <= (code) and (code) <= 0xFF)
def IS_SYSTEM(code): return (KC_PWR <= (code) and (code) <= KC_WAKE)
def IS_CONSUMER(code): return (KC_MUTE <= (code) and (code) <= KC_BRID)
def IS_FN(code): return (KC_FN0 <= (code) and (code) <= KC_FN31)


def layer(code):
    if code & 0x8000:
        return (code & 0x6000) >> 13
    else:
        return 0


def tap(code):
    return code & 0x1FFF


def hold(code):
    if code & 0x2000:
        return code & 0x1FFF
    else:
        layer(code)


def LT(layer, key):
    return 0x8000 | (layer << 13) | key


def MT(mkey, key):
    # Mods:   43210
    #   bit 0 ||||+- Control
    #   bit 1 |||+-- Shift
    #   bit 2 ||+--- Alt
    #   bit 3 |+---- Gui
    #   bit 4 +----- LR flag(Left: 0, Right: 1)
    mod = 0
    if IS_MOD(mkey):
        if mkey == 0xE0:
            mod |= 1
        if mkey == 0xE1:
            mod |= 2
        if mkey == 0xE2:
            mod |= 4
        if mkey == 0xE3:
            mod |= 8
        if mkey == 0xE4:
            mod = mod | 0x11
        if mkey == 0xE5:
            mod = mod | 0x12
        if mkey == 0xE6:
            mod = mod | 0x14
        if mkey == 0xE7:
            mod = mod | 0x18
        return 0x2000 | (mod << 8) | key
    else:
        return 0


def C(code):  # Control
    return 0x0100 | code


def S(code):  # Shift
    return 0x0200 | code


def A(code):  # Alt / Option
    return 0x0400 | code


def G(code):  # Gui / Cmd
    return 0x0800 | code
