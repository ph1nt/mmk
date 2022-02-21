import time
from machine import Pin
from machine import Timer
from keycode import layer
from keys import key


class Matrix:
    """
    Implement the scan of keyboard matrix
    """

    ROWS = (5, 18, 23, 19)
    COLS = (13, 15, 2, 34, 4, 25, 26, 27, 14, 12)  # 2,0,4

    def __init__(self):
        key_timer = Timer(0)
        #key_timer.init(period=1, mode=Timer.PERIODIC, callback=lambda t: self.scan(self))
        self.keys = len(self.ROWS) * len(self.COLS)
        self.queue = bytearray(self.keys)
        self.head = 0
        self.tail = 0
        self.length = 0
        self.state = []  # list of currently pressed keys
        self.rows = []  # row as output
        for row in self.ROWS:
            io = Pin(row, Pin.OUT)
            io.value(0)
            self.rows.append(io)
        self.cols = []  # col as input
        for col in self.COLS:
            io = Pin(col, Pin.IN, Pin.PULL_DOWN)
            self.cols.append(io)
        # row selected value depends on diodes' direction
        self.last = [0] * self.keys  # key last status
        self.debounce = [0] * self.keys  # key hold state
        self.matrix = [0] * self.keys  # key current state
        self._debounce_time = 20  # 20 ms
        self._hold_time = 200  # 500 ms

    def scan(self):
        """
        Scan keyboard matrix run from Timer(0)
        four states of key:
        - free      pin.value == 0
        - debounce  wait for stabilisation
        - tap       single press and release
        - hold      hold some time
        """
        time_ms = time.time_ns() / 1000000
        key_index = -1
        for row in self.rows:
            row.value(1)  # select row
            for col in self.cols:
                key_index += 1
                current = col.value()  # check column
                if current != self.last[key_index]:
                    self.debounce[key_index] = time_ms
                self.last[key_index] = current
                if (time_ms - self.debounce[key_index]) > self._debounce_time:
                    if current == 0:
                        if self.matrix[key_index] == 1:
                            self.matrix[key_index] = 3
                        else:
                            self.matrix[key_index] = 0
                    else:
                        if (time_ms - self.debounce[key_index]) > self._hold_time:
                            # hold detected
                            self.matrix[key_index] = 2
                        else:
                            self.matrix[key_index] = 1
                    # 0 key up (free); 1 down; 2 hold; 3 pressed
            row.value(0)

    def decode(self):
        self.state = []
        cur_layer = 0
        for idx, val in enumerate(self.matrix):
            if val > 1:
                print('key:{} idx:{} val:{}'.format(hex(key(cur_layer, idx)), idx, val))

    def costam():
        for idx, val in enumerate(self.matrix):
            # scan for layers
            if val == 2:
                print('key:{}'.format(hex(key(cur_layer, idx))))
                if key(cur_layer, idx) and 0x8000:
                    cur_layer = layer(key(cur_layer, idx))
                    print('ustawiono warstwę {}'.format(cur_layer))
            pass
        for idx, val in enumerate(self.matrix):
            # scan for modifiers
            if val == 2:
                if key(cur_layer, idx) and 0x0F00:
                    pass
            pass
        for idx, val in enumerate(self.matrix):
            # scan for keys
            if idx == 3:
                self.state.append(key(cur_layer, idx) and 0x00FF)
                # append SHIFT or other modifiers in current key
        print('layer:{} stan:{}'.format(cur_layer, self.state))

    @property
    def debounce_time(self):
        return self._debounce_time

    @debounce_time.setter
    def debounce_time(self, _t):
        """Set debounce time"""
        self._debounce_time = _t

    @property
    def hold_time(self):
        return self._hold_time

    @debounce_time.setter
    def hold_time(self, _t):
        """Set hold time"""
        self._hold_time = _t
