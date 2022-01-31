from gc import callbacks
import time
from machine import Pin
from machine import Timer


class Matrix:
    """
    Implement the scan of keyboard matrix
    """

    # ROWS = (P0_05, P0_06, P0_07, P0_08, P1_09, P1_08, P0_12, P0_11)
    # COLS = (P0_19, P0_20, P0_21, P0_22, P0_23, P0_24, P0_25, P0_26)
    ROWS = ()
    COLS = ()
    # direction of diode
    ROW2COL = False

    def __init__(self):
        key_timer = Timer(0)
        key_timer.init(
            period=1, mode=Timer.PERIODIC, callback=lambda t: self.scan(self)
        )
        self.keys = len(self.ROWS) * len(self.COLS)
        self.queue = bytearray(self.keys)
        self.head = 0
        self.tail = 0
        self.length = 0
        self.rows = []  # row as output
        for pin in self.ROWS:
            io = Pin(pin, Pin.OUT, Pin.PUSH_PULL)
            io.value(0)
            self.rows.append(io)
        self.cols = []  # col as input
        for pin in self.COLS:
            io = Pin(pin, Pin.IN, Pin.PULL_DOWN if self.ROW2COL else Pin.PULL_UP)
            self.cols.append(io)
        # row selected value depends on diodes' direction
        self.pressed = bool(self.ROW2COL)
        self.last = [0] * self.keys  # key last status
        self.hold = [0] * self.keys  # key hold state
        self.matrix = [0] * self.keys  # key current state
        self._debounce_time = 20  # 20 ms
        self._hold_time = 500  # 500 ms

    def scan(self):
        """
        Scan keyboard matrix run from Timer(0)
        four states of key:
        - free      pin.value == 0
        - debounce  wait for stabilisation
        - tap       single press and release
        - hold      hold some time
        """
        time_ms = time.monotonic_ns() / 1000000
        key_index = -1
        for row in self.rows:
            row.value = self.pressed  # select row
            for col in self.cols:
                key_index += 1
                current = col.value != self.pressed  # check column
                if current != self.last[key_index]:
                    self.debounce = time_ms
                self.last[key_index] = current
                if time_ms - self.debounce > self._debounce_time:
                    if time_ms - self.debounce > self._hold_time:
                        # hold detected
                        if current == 1:
                            current = 2
                    # 0 free; 1 pressed; 2 hold
                    self.matrix[key_index] = current
            row.value = not self.pressed

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
