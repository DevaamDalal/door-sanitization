# Bill of materials

Quantities describe one controller for two doors. The list distinguishes parts reported in the working prototype from items still needed for a robust build.

| Qty | Part | Value / specification | Status |
| ---: | --- | --- | --- |
| 1 | Arduino Nano | Classic ATmega328P, 5 V | Installed |
| 1 | Voltage regulator | 7805 from 24 V to 5 V | Installed; thermal design unverified |
| 1 | Input capacitor | 1 uF across IN and GND, adequate voltage rating | Installed |
| 1 | Output capacitor | 0.1 uF across OUT and GND | Installed |
| 2 | Proximity sensor | E18-D80NK, tested active LOW | Installed |
| 3 | Logic-level N-channel MOSFET | IRLZ44N, TO-220 G-D-S | Installed |
| 3 | Gate series resistor | 330 ohm | Installed |
| 3 | Gate pulldown resistor | 10 kohm | Installed |
| 1 | Pump | 24 V DC; current rating to be confirmed | Connected and reported working |
| 2 | Solenoid valves | 24 V DC; current rating to be confirmed | Connected and reported working |
| 1 | Supply rail diode | Unspecified diode across 24 V/GND | Reported installed; value/orientation unverified |
| 3 | Load flyback clamp | One per pump/valve, chosen for measured load current and switching energy | **Not installed** |
| 1 | Supply fuse and holder | Size for cable and actual load current | Recommended; installation unverified |
| 1 | 24 V source | Supply rated for pump startup plus both valves | In use; ratings unverified |
| As needed | Power connectors/wire | Rated for the actual pump/valve currents | Installed in prototype |
| 1 | Controller enclosure | Insulated with appropriate strain relief and mist protection | Recommended for permanent use |

The 330 ohm values reflect the assembled board; an older prototype note mentioned 100–220 ohm and should not be used as the wiring reference. Likewise, the installed 7805 is different from a recommended buck-converter upgrade.
