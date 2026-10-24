# Test record and troubleshooting

## Reported milestones

The builder reported a successful breadboard IRLZ44N check with a corrected series resistor, successful DMM continuity/resistance checks, resolution of an accidental RESET-to-GND short, then that the final code and circuit worked together. These are user reports, not independently witnessed measurements. The separate load protection and regulator thermal performance have not been validated.

A passive board check previously reported all ground points below 1 ohm; each Nano D5/D6/D7 to its MOSFET gate about 330 ohm; a gate pulldown about 9.81 kohm after removing the Nano. These readings are illustrative, not acceptance measurements for a different board.

## Quick functional check

1. Power off both USB and 24 V before any wiring or ohms/continuity measurement.
2. With loads disconnected, verify regulator OUT is connected to Nano 5V and not VIN; check for shorts between 24 V, 5 V and GND.
3. With only 24 V connected, check supply positive to ground and Nano 5V to ground. Stop if the regulator output is outside the Nano/sensor supply range or the 7805 becomes excessively hot.
4. Before operating inductive loads, fit and check an appropriately rated clamp across each pump/valve. A diode across the supply rails does not serve this role.
5. On boot with a sensor blocked, confirm no output until the sensor has cleared and been triggered again.
6. Trigger sensor 1 and check D6 and D5; trigger sensor 2 and check D7 and D5. Each pulse lasts about 1 s, with a 4 s cooldown. Both channels can overlap.
7. Hold one sensor blocked beyond its cooldown: it should not repeat until that sensor clears and detects again.

## Upload failure that was resolved

The sketch compiled but avrdude showed programmer is not responding / not in sync. Upload worked with the Nano removed from its socket. In the unpowered empty socket, RST-to-GND measured around 0.4 ohm; the builder removed this short. A RESET pin held low prevents normal boot/upload. For recurrence, remove power, pull the Nano, check socket RST-to-GND resistance and inspect bridges/socket alignment. Then check the correct Nano board, processor and COM port. Use resistance mode only with USB and 24 V disconnected.

## Practical limits

No tank float switch or dry-run protection is implemented; D4 is reserved. No independent watchdog, load-current monitor, valve-position feedback or hardware cutoff is present. Software cannot interrupt a MOSFET failed short. The E18-D80NK range was found too short for the user's desired sensing distance. A different sensor can require a different supply, interface and firmware; do not connect a 24 V sensor output to the Nano without verifying its output voltage and logic.
