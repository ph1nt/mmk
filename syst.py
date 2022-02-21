import esp32


class Syst():
    def __init__(self) -> None:
        pass

    def temperature(self):  # read the internal temperature of the MCU
        return round((esp32.raw_temperature() - 32) / 1.8)

    def hall(self):  # read the internal hall sensor
        return esp32.hall_sensor()

# esp32.ULP()             # access to the Ultra-Low-Power Co-processor
