import esp32
from machine import sleep, deepsleep, Pin


class Syst():
    ROWS = (5, 18, 23, 19)
    COLS = (13, 15, 2, 34, 4, 25, 26, 27, 14, 12)

    def __init__(self) -> None:
        self.rows = []  # row as output
        for row in self.ROWS:
            io = Pin(row, Pin.OUT)
            self.rows.append(io)
        self.cols = []  # col as input
        for col in self.COLS:
            io = Pin(col, Pin.IN, Pin.PULL_DOWN)
            self.cols.append(io)
        pass

    def temperature(self):  # read the internal temperature of the MCU
        return round((esp32.raw_temperature() - 32) / 1.8)

    def hall(self):  # read the internal hall sensor
        return esp32.hall_sensor()

    def sleep(self):
        print('going sleep')
        for row in self.rows:
            row.value(1)
        esp32.wake_on_ext1(pins=(Pin(34),), level=esp32.WAKEUP_ANY_HIGH)
        sleep()
        for col in self.cols:
            print('{} {}'.format(col, col.value()))
        print('dzemka ;)')
        # deepsleep(10000)
        for col in self.COLS:
            io = Pin(col, Pin.IN, Pin.PULL_DOWN)
        for row in self.rows:
            row.value(0)
# esp32.ULP()             # access to the Ultra-Low-Power Co-processor
