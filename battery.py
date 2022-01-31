from machine import ADC

adc = ADC(Pin(32), atten=ADC.ATTEN_11DB)  # create ADC object for pin 32
adc.read_u16()  # read raw value, 0-65535
