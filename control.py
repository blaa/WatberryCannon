import pygame
import config
from time import time

class Control(object):
    """
    Control loop for steering robot and pump via joystick
    """

    def __init__(self, joystick, pump, robot):
        "Set up state"
        self.joystick = joystick
        self.pump = pump
        self.robot = robot

        # Is robot/servos/pump enabled? Special joystick key enables robot so it won't kill anyone.
        self.is_robot_on = False
        # Are we in fire mode? (Pump might be in intermittent mode - not pumping this instance)
        self.is_fire = False
        # Is pulse/intermittent mode enabled?
        self.is_pulse = False

    # Actions
    def _do_turn_on(self):
        "Turn robot/pump/control ON"
        self.is_robot_on = True
        self.is_pump_on = False
        self.robot.enable()
        print "Control: Turned on"

    def _do_turn_off(self):
        "Disable robot and robot/servos and pump"
        self.pump.off()
        self.robot.disable()
        self.is_robot_on = False
        self.is_fire = False
        print "Control: Turned off"

    def _do_fire_start(self):
        "Enable firing (intermittent or constant)"
        self.pump.on()
        self.is_fire = True
        self.fire_start = time()

    def _do_fire_stop(self):
        "Cease fire"
        self.pump.off()
        self.is_fire = False

        pos = self.robot.get_position()
        took = time() - self.fire_start
        print "Control: Fire ceased at %s with power %.2f after %.2f seconds" % (
            pos, self.pump.power, took
        )

    def _do_move_robot(self):
        "Update servos angles"
        x = self.joystick.get_axis(config.AXIS_X)
        y = self.joystick.get_axis(config.AXIS_Y)
        w = 0

        power = self.joystick.get_axis(config.AXIS_POWER)
        power = (power + 1.0) / 2.0
        self.pump.set_power(power)
        # Those *, +, and - depend on robot construction
        self.robot.set(x * 70, - w * 70, -20 + y * 70)

    def loop(self):
        "Joystick -> (Pump, Robot) control"

        print "- Entering control loop (HIDE!)"
        while True:
            try:
                event = pygame.event.wait()
            except KeyboardInterrupt:
                break

            # Good for checking button numbers (try jstest)
            #print "BUTTS", [self.joystick.get_button(i) for i in range(0, self.joystick.get_numbuttons())]

            # Check on/off event
            if event.type == pygame.JOYBUTTONDOWN and event.button == config.BUTTON_ON_OFF:
                if self.is_robot_on is False:
                    # Enable
                    self._do_turn_on()
                else:
                    self._do_turn_off()

            if self.is_robot_on is False:
                continue

            # Robot is enabled - handle actions

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == config.BUTTON_FIRE:
                    self._do_fire_start()
                elif event.button == config.BUTTON_PULSE:
                    self.is_pulse = not self.is_pulse
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == config.BUTTON_FIRE:
                    self._do_fire_stop()
            elif event.type == pygame.JOYAXISMOTION:
                self._do_move_robot()
            elif event.type == pygame.USEREVENT: # Timer tick
                if self.is_pulse and self.is_fire:
                    if self.pump.is_on is False:
                        self.pump.on()
                    else:
                        self.pump.off()
            elif event.type == pygame.QUIT:
                break

        print "Finishing on user request"
