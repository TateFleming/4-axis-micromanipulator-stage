This folder contains the photos of the setup without the stage (arduino, drivers, enclosure, motors, etc.). The actual stage consists of 3 micrometers magnetically connected to a block that can translate in the x, y, and z directions by rotating the micrometers. The coupling.jpg shows what is used to connect the stepper motors to the micrometers. The couplers are flexible and can withstand more torque than the stepper motors can provide, which is significantly more than the amount required to rotate the micrometers.

The enclosure was machined to include holes for the power supply connections, USB connection, DB32 connector, and standoffs for the board and drivers.

A metal plate was machined to hold the stepper motors. Bolts with rubber feet are attached to the plate to keep the motors from contacting whatever surface they're on to prevent vibrations.

Connections:
- All grounds connected.
- The M+ of each driver is connected to the positive terminal of the power supply.
- The Enable, MS1, MS2, MS3, Step, and Direction pins of each board are connected to digital pins of the arduino mega.
- The A and B pins on the drivers are soldered to the male DB32 connector attached to the enclosure.
- The wires of the stepper motors are soldered to the female DB32 connector to match the connections of the male connector.
