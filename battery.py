'''Reads voltage on pin ADC1_7 next convert it to battery percent level of charge'''
from machine import Pin, ADC

batteryPin = Pin(35)  # Pin 11 ADC1_7
battery_in = ADC(batteryPin)
battery_in.atten(battery_in.ATTN_11DB)


def battery_level():
    '''
    Read ADC pin with battery voltage via divider 91K/91K

    Return:
    battery level in percents
    '''
    batt_lvl = ([1757, 1], [1842, 2], [1893, 3], [1946, 4], [1978, 5], [1994, 6], [2002, 7], [2009, 8], [2019, 9], [2031, 10], [2037, 11], [2043, 12], [2050, 13], [2061, 14], [2065, 15], [2071, 16], [2077, 18], [2083, 19], [2089, 22], [2095, 25], [2100, 28], [2106, 32], [2109, 36], [2112, 40], [2115, 44], [2119, 47], [2127, 51], [2133, 53], [2140, 56], [2146, 58], [2152, 60], [
        2157, 62], [2161, 64], [2165, 66], [2169, 67], [2173, 69], [2178, 71], [2183, 72], [2187, 74], [2193, 76], [2197, 77], [2202, 79], [2206, 81], [2211, 82], [2215, 84], [2220, 85], [2234, 86], [2245, 87], [2249, 88], [2262, 89], [2269, 90], [2273, 91], [2282, 92], [2289, 93], [2294, 94], [2300, 95], [2304, 96], [2309, 97], [2314, 98], [2321, 99], [2327, 100])
    adc_batt = battery_in.read()
    for level_idx, batt_val in enumerate(batt_lvl):
        if adc_batt > batt_lvl[level_idx][0]:
            pass
        else:
            return batt_lvl[level_idx][1]
    return 100


'''
ADC readings to battery level to battery voltage
ADC:1757, level:1%, volt:3119mV
ADC:1842, level:2%, volt:3271mV
ADC:1893, level:3%, volt:3352mV
ADC:1946, level:4%, volt:3416mV
ADC:1978, level:5%, volt:3469mV
ADC:1994, level:6%, volt:3497mV
ADC:2002, level:7%, volt:3516mV
ADC:2009, level:8%, volt:3533mV
ADC:2019, level:9%, volt:3551mV
ADC:2031, level:10%, volt:3569mV
ADC:2037, level:11%, volt:3577mV
ADC:2043, level:12%, volt:3586mV
ADC:2050, level:13%, volt:3595mV
ADC:2061, level:14%, volt:3614mV
ADC:2065, level:15%, volt:3622mV
ADC:2071, level:16%, volt:3632mV
ADC:2077, level:18%, volt:3640mV
ADC:2083, level:19%, volt:3650mV
ADC:2089, level:22%, volt:3658mV
ADC:2095, level:25%, volt:3668mV
ADC:2100, level:28%, volt:3676mV
ADC:2106, level:32%, volt:3686mV
ADC:2109, level:36%, volt:3694mV
ADC:2112, level:40%, volt:3704mV
ADC:2115, level:44%, volt:3714mV
ADC:2119, level:47%, volt:3721mV
ADC:2127, level:51%, volt:3730mV
ADC:2133, level:53%, volt:3739mV
ADC:2140, level:56%, volt:3749mV
ADC:2146, level:58%, volt:3757mV
ADC:2152, level:60%, volt:3767mV
ADC:2157, level:62%, volt:3777mV
ADC:2161, level:64%, volt:3785mV
ADC:2165, level:66%, volt:3795mV
ADC:2169, level:67%, volt:3803mV
ADC:2173, level:69%, volt:3811mV
ADC:2178, level:71%, volt:3821mV
ADC:2183, level:72%, volt:3829mV
ADC:2187, level:74%, volt:3838mV
ADC:2193, level:76%, volt:3847mV
ADC:2197, level:77%, volt:3856mV
ADC:2202, level:79%, volt:3866mV
ADC:2206, level:81%, volt:3874mV
ADC:2211, level:82%, volt:3884mV
ADC:2215, level:84%, volt:3894mV
ADC:2220, level:85%, volt:3902mV
ADC:2234, level:86%, volt:3920mV
ADC:2245, level:87%, volt:3948mV
ADC:2249, level:88%, volt:3956mV
ADC:2262, level:89%, volt:3973mV
ADC:2269, level:90%, volt:3982mV
ADC:2273, level:91%, volt:3991mV
ADC:2282, level:92%, volt:4009mV
ADC:2289, level:93%, volt:4019mV
ADC:2294, level:94%, volt:4027mV
ADC:2300, level:95%, volt:4037mV
ADC:2304, level:96%, volt:4045mV
ADC:2309, level:97%, volt:4055mV
ADC:2314, level:98%, volt:4063mV
ADC:2321, level:99%, volt:4073mV
ADC:2327, level:100%, volt:4081mV
'''
