from time import time_ns
from ssd1306 import *
from machine import Pin, SoftI2C


class Disp(SSD1306_I2C):
    def __init__(self, width=128, height=32, _sda=32, _scl=33, addr=0x3C):
        i2c = SoftI2C(sda=Pin(_sda), scl=Pin(_scl))
        self.update = time_ns
        super().__init__(width, height, i2c, addr=0x3C, external_vcc=False)

    def logo(self):
        self.fill(0)
        self.fill_rect(0, 0, 32, 32, 1)
        self.fill_rect(2, 2, 28, 28, 0)
        self.vline(9, 8, 22, 1)
        self.vline(16, 2, 22, 1)
        self.vline(23, 8, 22, 1)
        self.fill_rect(26, 24, 2, 4, 1)
        self.text('MicroPython', 40, 0, 1)
        #self.text('SSD1306', 72, 12, 1)
        self.text('OLED 128x32', 40, 24, 1)
        self.contrast(0)
        self.show()

    def battery(self, level, voltage):
        bat_str = str(level) + '% ' + str(voltage) + 'mV '
        self.fill_rect(40, 12, 87, 8, 0)
        self.text(bat_str, 40, 12, 1)
        self.show()

    def brightness(self, value):
        self.fill_rect(0, 31, value * 8, 31, 1)
        self.fill_rect(value * 8, 31, 127, 31, 0)
        self.contrast(value * 8)
        self.show()
