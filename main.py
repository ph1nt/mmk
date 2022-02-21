from rotary_irq_esp import RotaryIRQ
from time import sleep_ms
from machine import Pin, SoftI2C
from ssd1306 import *
from battery import battery_level, battery_voltage
from matrix import Matrix

matrix = Matrix()
# using default address 0x3C
i2c = SoftI2C(sda=Pin(32), scl=Pin(33))
display = SSD1306_I2C(128, 32, i2c)

display.fill(0)
display.fill_rect(0, 0, 32, 32, 1)
display.fill_rect(2, 2, 28, 28, 0)
display.vline(9, 8, 22, 1)
display.vline(16, 2, 22, 1)
display.vline(23, 8, 22, 1)
display.fill_rect(26, 24, 2, 4, 1)
display.text('MicroPython', 40, 0, 1)
#display.text('SSD1306', 72, 12, 1)
display.text('OLED 128x32', 40, 24, 1)
display.contrast(0)
display.show()

r = RotaryIRQ(pin_num_clk=17,
              pin_num_dt=16,
              min_val=0,
              max_val=15,
              reverse=True,
              pull_up=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

val_old = r.value()
bat_old = 0
bat_new = 0
time_out = 0
display.poweroff()
print('keeb main loop')
while val_old != 5:
    matrix.scan()
    matrix.decode()
    val_new = r.value()
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
    sleep_ms(5)
print('The End')
quit()

val_new = r.value()
if time_out == 100:
    bat_new = battery_level()
    time_out = 0

if bat_old != bat_new:
    bat_str = str(bat_new) + '% ' + str(battery_voltage()) + 'mV '
    display.fill_rect(40, 12, 87, 8, 0)
    display.text(bat_str, 40, 12, 1)
    #print('battery level: {}'.format(bat_str))
    display.show()
if val_old != val_new:
    val_old = val_new
    print('result =', val_new)
    display.fill_rect(0, 31, val_new * 8, 31, 1)
    display.fill_rect(val_new * 8, 31, 127, 31, 0)
    display.contrast(val_new * 8)
    display.show()
    if time_out > 120:
        display.invert(0)
        display.poweron()
    time_out = 0
sleep_ms(5)
time_out += 1
if time_out > 100:
    display.invert(1)
    if time_out > 120:
        display.poweroff()
# keyboard scan
matrix.scan()
