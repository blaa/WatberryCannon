#!/usr/bin/env python

"""
2-servo 1-pump Water cannon controller with a joystick.
If it doesn't work - my pygame required root. Somehow.

You probably need to recalibrate Robot to suite your setting.
My joystick allowed me to configure pump power using throttle.
"""

from time import sleep
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pigpio

import pygame

from robot import Robot
from pump import Pump
from control import Control
from IPython import embed

import config

def init_pygame():
    "Pygame initialization + debug"
    print "- Initialize pygame"
    pygame.init()
    #print "Initialize display"
    #pygame.display.init()
    #pygame.display.set_mode((1,1))
    print "- Initialize joystick"
    pygame.joystick.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    axes = joystick.get_numaxes()
    hats = joystick.get_numhats()
    buts = joystick.get_numbuttons()
    print "  AXES: %d HATS: %d BUTS: %d" % (axes, hats, buts)

    # Better handling of keyboard interrupt
    # And pulse firing.
    pygame.time.set_timer(pygame.USEREVENT, 200)
    return joystick


def main():
    try:
        joystick = init_pygame()
    except Exception:
        print "Pygame initialization failed - it MIGHT require (for unknown reasons) root"
        print "You can try with root, but that won't be safer"
        print
        raise

    pi = pigpio.pi()

    pump = Pump(pi, pin=config.PIN_PUMP)
    pump.off()
    robot = Robot(pi, config.PIN_SERVO1, config.PIN_SERVO2, config.PIN_SERVO3)
    robot.disable()

    control = Control(joystick, pump, robot)
    try:
        control.loop()
    finally:
        pump.off()


if __name__ == "__main__":
    main()
