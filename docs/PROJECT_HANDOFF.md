# Project handoff

This file preserves the essential context for continuing Door Sanitization without the original chat. Read README.md, docs/wiring.md, docs/bom.md, and the sketch before making changes. This is a project summary, not an electrical certification.

## Original objective

Detect a person entering or leaving a room and trigger a timed spray through a shared pump and the corresponding door’s solenoid valve. The prototype has two independent sensor and valve channels.

The builder reported that the circuit and code work together. No spray substance, exposure method, effectiveness, or safety for use on people has been validated. Keep testing to contained water only, away from people, until those questions are independently resolved.

## Hardware as reported by the builder

- Controller: classic 5 V Arduino Nano (ATmega328P).
- Supply: 24 V DC. A 7805 supplies the Nano **5V pin** and sensors; Nano VIN is unused. There is a 1 µF capacitor at the regulator input and a 0.1 µF capacitor at its output.
- Sensors: two 5 V E18-D80NK units, tested active LOW with NPN open-collector outputs. Sensor 1 OUT → D2; sensor 2 OUT → D3. Firmware uses INPUT_PULLUP.
- Outputs: D5 controls the pump, D6 controls door 1’s valve, and D7 controls door 2’s valve.
- Each output drives an IRLZ44N Gate through **330 Ω**. Each Gate has a **10 kΩ** resistor to its Source/GND. Each MOSFET Drain connects to its load negative; load positives connect to 24 V.
- D4 is reserved for a future tank-level input. No tank-level shutdown is implemented.
- A diode across the 24 V supply rails was reported installed. **Individual flyback diodes across the pump and two valves were not installed** at the time of the report. The rail diode does not replace them.

## Firmware behavior

The working sketch is `DoorSanitization/DoorSanitization.ino`.

Each door operates independently. A sensor must be clear for 200 ms to arm. Detection lasting 40 ms starts a 1-second valve pulse, followed by a 4-second cooldown. The door must clear before it can trigger again. The pump runs whenever either door is spraying, including when both cycles overlap. A sensor blocked at startup must clear before it can trigger.

## Troubleshooting history

The sketch compiled, but uploading initially failed when the Nano was in its circuit-board socket. Uploading worked when the Nano was removed. With all power disconnected and the Nano out, socket RST-to-GND measured approximately **0.4 Ω**. The builder fixed that short, resolving the upload issue.

If this failure returns, check the RST socket contact, nearby solder, and Nano alignment before changing the sketch. Use resistance or continuity mode only with both USB and 24 V disconnected.

The E18-D80NK’s practical sensing range was too short for the intended placement. No replacement sensor has been selected. A replacement powered by 24 V needs its output voltage and interface verified before its signal is connected to Nano D2 or D3.

## Outstanding work

- Fit appropriately rated and correctly oriented suppression across **each** inductive load. Choose parts after checking the pump and valve currents.
- Measure the 7805’s output voltage and temperature with the complete system operating. Dropping 24 V to 5 V can produce substantial heat; consider a properly rated buck converter.
- Verify fuse installation, wire and connector ratings, enclosure, and protection from moisture.
- Add tank-empty protection if the pump could run dry. The current system has no independent maximum-on cutoff, valve feedback, or protection against a MOSFET failing short.
- Choose and test a longer-range sensor at the actual doorway before changing the sensor wiring or firmware.

## Continuing from another computer

Clone this GitHub repository and open `DoorSanitization/DoorSanitization.ino` in Arduino IDE. Select the correct Nano board, processor, and port. Commit and push future changes so the repository stays current.

Git preserves committed code and documentation. It does **not** automatically preserve changes to the physical board, new measurements, unattached photos, Arduino IDE settings, or the exact messages in the original chat. Record important new findings here as they are verified.
