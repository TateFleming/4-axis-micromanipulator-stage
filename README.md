# 4-axis-micromanipulator-stage

Background: This repository contains information of a project I worked on during my research at Appalachian State University under Dr. Francois Amet. The research consists of superconductivity in graphene and other novel 2-D materials. The microscopic devices used in our research are initially assembled under an optical microscope on a multiaxis stage. Graphene devices can be created in open air because they do not oxidize very quickly. Niobium diselenide (NbSe2) oxidizes rather quickly and requires a vacuum glove box for device assembly in our research. The glove box maintains a better vacuum when the gloves are used as little as possible, so the goal of this project was to create a four-axis micromanipulator stage that could be controlled by a computer rather than manually.

Required materials:
- Four-axis stage
- Stepper motors (4) *used Model: 42BYGHM809
- Big Easy Driver (4) *or 1 driver and multiplex the motors or shift register
- Arduino Mega *could possibly use Uno if you multiplex the motors with one driver
- Current supply *used 12V 10A DC supply at ~2A
- flexible coupling for the motors to the micrometers

Optional materials:
- DB32 male connector
- DB32 female connector
- Enclosure for the arduino and drivers
- Metal plate to secure the motors
- Vibration absorbing legs for the metal plate

Software:
- Arduino
- Python *or Processing

Arduino Libraries:
- Firmata

Python Libraries:
- TKinter
- PyFirmata
- Time
