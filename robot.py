#!/usr/bin/env python

class Robot(object):
    """
    Control 3-servo arm-like robot using angles.
    """
    def __init__(self, pi, servo1_pin=25, servo2_pin=24, servo3_pin=23):
        self.servo1 = servo1_pin
        self.servo2 = servo2_pin
        self.servo3 = servo3_pin

        # PWM edge values
        self.start = 700
        self.stop = 2400

        # PWM middle - angle 0
        self.middle = (self.stop - self.start)/2 + self.start
        self.pi = pi

        # Debug / display
        self.angle_1 = 0
        self.angle_2 = 0
        self.angle_3 = 0

    def enable(self):
        "Enable PWMS/servo control"
        self.pi.set_servo_pulsewidth(self.servo1, self.middle)
        self.pi.set_servo_pulsewidth(self.servo2, self.middle)
        self.pi.set_servo_pulsewidth(self.servo3, self.middle)

    def disable(self):
        "Disable servo control completely"
        self.pi.set_servo_pulsewidth(self.servo1, 0)
        self.pi.set_servo_pulsewidth(self.servo2, 0)
        self.pi.set_servo_pulsewidth(self.servo3, 0)

    def _map_angle(self, angle):
        "Map (-90 - 90) angle to PWM values"
        # -90 - start
        # 90 - stop
        # 0 - middle
        if angle > 90:
            angle = 90
        elif angle < -90:
            angle = -90

        angle += 90
        # Angle from 0 to 180
        angle /= 180.0
        # Angle = 0 to 1
        angle *= self.stop - self.start
        angle += self.start
        return angle

    def set(self, s1, s2, s3):
        "Set robot position"
        self.angle_1, self.angle_2, self.angle_3 = s1, s2, s3
        self.pi.set_servo_pulsewidth(self.servo1, self._map_angle(s1))
        self.pi.set_servo_pulsewidth(self.servo2, self._map_angle(s2))
        self.pi.set_servo_pulsewidth(self.servo3, self._map_angle(s3))

    def get_position(self):
        return "angles: %.2f %.2f %.2f" % (self.angle_1, self.angle_2, self.angle_3)


def test():
    "Simple test of edge angles"
    from time import sleep
    robot = Robot()
    robot.enable()
    sleep(1)

    try:
        while True:
            current = -90.
            while True:
                robot.set(current, current, current)

                print current
                current += 2

                if current >= 90:
                    sleep(1)
                    current = -90
                    robot.set(current, current, current)
                    sleep(2)

                sleep(0.1)
    finally:
        robot.disable()


if __name__ == "__main__":
    test()
