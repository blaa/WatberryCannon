
class Pump(object):
    """
    Control pump on/off and it's power using a PWM and a MOSFET.
    """
    def __init__(self, pi, pin=18):
        self.pump_pin = pin
        self.pi = pi

        self.off()

        # From 0 to 255 - internal
        self.conv_power = 0
        # From 0 to 1 - input
        self.power = 0

    def on(self):
        "Pump on"
        self.pi.set_PWM_dutycycle(self.pump_pin, self.conv_power)
        self.is_on = True

    def off(self):
        "Pump off"
        self.pi.set_PWM_dutycycle(self.pump_pin, 0)
        self.is_on = False

    def set_power(self, power):
        "Set pump power"
        conv_power = power * 255
        if conv_power >= 250:
            conv_power = 255
        conv_power = int(conv_power)
        if self.conv_power == conv_power:
            return
        self.conv_power = conv_power
        self.power = power
        if self.is_on is True:
            self.on()
