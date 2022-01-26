import time
from machine import Pin


class Matrix:
    """
    Implement the drive of keyboard matrix and provide an event queue.
    """

    # ROWS = (P0_05, P0_06, P0_07, P0_08, P1_09, P1_08, P0_12, P0_11)
    # COLS = (P0_19, P0_20, P0_21, P0_22, P0_23, P0_24, P0_25, P0_26)
    ROWS = ()
    COLS = ()

    # direction of diode
    ROW2COL = False

    def __init__(self):
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
        self._debounce_time = 20000000  # 20 ms
        self._hold_time = 500000000  # 500 ms

    def scan(self):
        """
        Scan keyboard matrix and save key event into the queue.
        //mamy cztery stany
        - free      pin.value == 0
        - debounce  wait for stabilisation
        - tap       single press and release
        - hold      hold some time
        :return: length of the key event queue.
        """
        t = time.monotonic_ns()
        # use local variables to speed up
        key_index = -1
        for row in self.rows:
            row.value = self.pressed  # select row
            for col in self.cols:
                key_index += 1
                current = col.value != self.pressed
                if current != self.last[key_index]:
                    self.debounce = t
                self.last[key_index] = current
                if t - self.debounce > self._debounce_time:
                    if t - self.debounce > self._hold_time:
                        # hold detected
                        if current == 1:
                            current = 2
                    # 0 free; 1 pressed; 2 hold
                    self.matrix[key_index] = current
            row.value = not self.pressed

    # TODO move to RTOS
    def wait(self, timeout=1000):
        """Wait for a new key event or timeout"""
        last = self.length
        if timeout:
            end_time = time.monotonic_ns() + timeout * 1000000
            while True:
                n = self.scan()
                if n > last or time.monotonic_ns() > end_time:
                    return n
        else:
            while True:
                n = self.scan()
                if n > last:
                    return n

    def put(self, data):
        """Put a key event into the queue"""
        self.queue[self.head] = data
        self.head += 1
        if self.head >= self.keys:
            self.head = 0
        self.length += 1

    def get(self):
        """Remove and return the first event from the queue."""
        data = self.queue[self.tail]
        self.tail += 1
        if self.tail >= self.keys:
            self.tail = 0
        self.length -= 1
        return data

    def time(self):
        """Return current time"""
        return time.monotonic_ns()

    def ms(self, t):
        """Convert time to milliseconds"""
        return t // 1000000

    @property
    def debounce_time(self):
        return self._debounce_time // 1000000

    @debounce_time.setter
    def debounce_time(self, t):
        """Set debounce time"""
        self._debounce_time = t * 1000000
