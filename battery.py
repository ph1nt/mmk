import microcontroller
import analogio

'''Reads voltage on pin ADC1_7 next convert it to battery percent level of charge'''
batteryPin = microcontroller.pin.GPIO35  # Pin 11 ADC1_7
BATTERY_LIMIT = 3100  # Cutoff voltage [mV].
BATTERY_FULLLIMIT = 4190  # Full charge definition [mV].
BATTERY_DELTA = 10  # mV between each element in the SoC vector.
BATTERY_VOLTAGE = (
    0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,
    2,  2,  2,  2,  2,  2,  2,  2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,
    4,  5,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 11, 12, 13, 13, 14, 15, 16,
    18, 19, 22, 25, 28, 32, 36, 40, 44, 47, 51, 53, 56, 58, 60, 62, 64, 66, 67, 69,
    71, 72, 74, 76, 77, 79, 81, 82, 84, 85, 85, 86, 86, 86, 87, 88, 88, 89, 90, 91,
    91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 100
)
battery_in = analogio.AnalogIn(batteryPin)


def battery_level():
    voltage = (3300 * battery_in.value) >> 15
    i = (voltage - BATTERY_LIMIT) // BATTERY_DELTA
    if i >= len(BATTERY_VOLTAGE):
        i = len(BATTERY_VOLTAGE) - 1
    elif i < 0:
        i = 0
    return BATTERY_VOLTAGE[i]
