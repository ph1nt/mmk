'''
MMK
'''
from syst import Syst
from rotary_irq_esp import RotaryIRQ
from time import ticks_ms, ticks_add, ticks_diff
from display import Disp
from battery import battery_level
from matrix import Matrix

matrix = Matrix()
display = Disp()
s = Syst()

print(s.temperature())

r = RotaryIRQ(pin_num_clk=17,
              pin_num_dt=16,
              min_val=0,
              max_val=15,
              reverse=True,
              pull_up=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

tBattery = 0
tEncoder = 0
tKeyboard = 0
tDisplay = ticks_add(ticks_ms(), 5000)
display.logo()
while True:
    t = ticks_ms()
    if ticks_diff(t, tBattery) > 0:
        display.battery(battery_level())
        tBattery = ticks_add(t, 500)
    if ticks_diff(t, tEncoder) > 0:
        display.brightness(r.value())
        tEncoder = ticks_add(t, 10)
    if ticks_diff(t, tKeyboard) > 0:
        matrix.scan()
        if matrix.decode() > 0:
            display.poweron()
            tDisplay = ticks_add(ticks_ms(), 5000)
        tKeyboard = ticks_add(t, 1)
    if ticks_diff(t, tDisplay) > 0:
        display.poweroff()

# TODO power safe
