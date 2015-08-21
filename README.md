
WatBerry Cannon
===============


Wat? WatBerry Cannon is a RasberryPI-powered joystick-controlled WATer
Cannon.

Have you got a non-zero number of plants at your house and a positive
number of unused rpis? Are you planning on leaving your desk for a few
days (let's assume you want to get to some remote geeky conference)?
Or maybe you just need to guard a high-security kitchen facility from
a local gang of cats?

If so - follow instructions.

1. Get yourself:
  - Some FET (IRLZ44) - or an overpriced rpi addon with motor control.
  - Connect it to some PWM pin (I used 18). Use pull-down resistor to prevent flooding.
  - Joystick (or not, you can use touch control from mobile).
  - Pump (for example a cheap car windshield washer pump or something funnier).
  - 2 servos to direct the hose at moving targets (or plants).
  - Python, pigpiod, pygame, GIT.
2. Combine stuff so that it works.
3. Run software.
4. Wat?
5. Fun.

Notes (to self):
- The water container should have an air intake otherwise pressure and stuff.
- Don't mistakenly switch joystick mode and wonder cluelessly what's wrong.
- Try not to brick the raspberry pi by connecting USB camera (how did
that even happen?!) or watering it.

Todos:
- Add camera motion detection and auto-aiming for extended fun.


![prototype](https://github.com/blaa/WatberryCannon/blob/master/gfx/rpi_water_cannon.jpg "Proud prototype")
