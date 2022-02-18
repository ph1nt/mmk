##from gc import callbacks
import time
from keyboard import KEYS_MAP
from numpy import matrix
from keycode import layer
from machine import Pin
from machine import Timer


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
        self.pressed = True
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
            row.value(self.pressed)  # select row
            for col in self.cols:
                key_index += 1
                current = col.value()  # check column
                if current != self.last[key_index]:
                    self.debounce[key_index] = time_ms
                self.last[key_index] = current
                if (time_ms - self.debounce[key_index]) > self._debounce_time:
                    if (time_ms - self.debounce[key_index]) > self._hold_time:
                        # hold detected
                        if current == 1:
                            current = 2
                    else:
                        if current == 0:
                            current = 3
                    # 0 key up (free); 1 down; 2 hold; 3 pressed
                    self.matrix[key_index] = current
                    # DEBUG
                    if current != 0:
                        print('key status {} at row {} col {}'.format(current, row, col))
            row.value(not self.pressed)

    def decode(self):
        self.state = []
        cur_layer = 0
        for idx in matrix:
            # scan for layers
            if self.matrix[idx] == 2:
                if layer(KEYS_MAP(cur_layer)[idx]):
                    cur_layer = layer(KEYS_MAP(cur_layer)[idx])
            pass
        for idx in matrix:
            # scan for modifiers
            if self.matrix[idx] == 3:
                if KEYS_MAP(cur_layer)[idx] and 0x0F00:
                    pass
            pass
        for idx in matrix:
            # scan for keys
            if self.matrix[idx] == 3:
                self.state.append(KEYS_MAP(cur_layer)[idx] and 0x00FF)
                # append SHIFT or other modifiers in current key

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
