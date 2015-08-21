#!/usr/bin/env python

"""
Instead of using a joystick control:
- program your plant placement (servo angles)
- amount of water (pump power and time)
- Add to cron

Notes:
Keep towels close by.
"""

from time import sleep
import os

import pigpio

from robot import Robot
from pump import Pump

# Use 'fire ceased' communications from joystick control to create this.
program = [
    # angle_a,angle_2, PUMP POWER, PUMP TIME
    [-37.53, -61.14, 0.5, 1],
    [9.38, -51.03, 1.0, 1.5],
    [58.45, -49.59, 0.3, 2],
    [12.99, -90.00, 0.6, 0.5],
]

ROBOT_DELAY = 0.4
PUMP_DELAY = 0.4

def main_loop():
    pi = pigpio.pi()
    pump = Pump(pi)
    pump.off()
    robot = Robot(pi)

    try:
        robot.enable()
        for x, y, power, volume in program:
            robot.set(x, 0, y)
            pump.set_power(power)
            sleep(ROBOT_DELAY)
            pump.on()
            sleep(volume)
            pump.off()
            sleep(PUMP_DELAY)
    finally:
        print "Disabling pump"
        pump.off()
        robot.disable()


if __name__ == "__main__":
    main_loop()
