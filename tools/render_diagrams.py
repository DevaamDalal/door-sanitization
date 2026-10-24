#!/usr/bin/env python3
"""Render the two editable SVG diagrams using only the Python standard library."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1] / "docs"
OUT.mkdir(exist_ok=True)

INK = "#19344b"
NAVY = "#102b41"
BLUE = "#2563a6"
ORANGE = "#c56719"
GREEN = "#17755c"
GRAY = "#526a7b"
PAPER = "#f5f8fb"

def rect(x, y, w, h, fill="white", stroke="#cbd8e3", rx=10, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def line(x1, y1, x2, y2, color=INK, sw=3, dash=""):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{sw}" stroke-dasharray="{dash}" fill="none" stroke-linecap="round"/>'

def path(d, color=INK, sw=3, dash=""):
    return f'<path d="{d}" stroke="{color}" stroke-width="{sw}" stroke-dasharray="{dash}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'

def txt(x, y, s, size=19, color=INK, weight=400, anchor="start"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, Segoe UI, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>'

def node(x, y, color=INK):
    return f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"/>'

def svg(w, h, content):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<rect width="{w}" height="{h}" fill="{PAPER}"/>'
            + "".join(content) + '</svg>\n')

p = []
p += [txt(44, 63, "OBERON MIST  |  circuit schematic", 34, NAVY, 700),
      txt(45, 95, "As-built: 24 V / 7805 / Nano / 2 sensors / 3 IRLZ44N. Orange dashed parts are still required.", 18, GRAY),
      rect(36, 126, 1740, 63, "#fff5e8", "#edc89c", 9, 1),
      txt(58, 165, "Load flyback clamps were NOT installed on the reported prototype. 24 V rail diode does not replace them.", 20, "#8d4411", 700)]

# Power block, global net names used rather than running ambiguous wires across blocks.
p += [rect(40, 218, 510, 415), txt(62, 253, "POWER  |  as built", 24, NAVY, 700),
      rect(63, 289, 112, 70, "#eaf2fb", BLUE), txt(80, 319, "J1", 17, BLUE, 700),
      txt(78, 345, "24 V DC", 18),
      rect(272, 291, 190, 95, "#e9f7f2", GREEN),
      txt(301, 325, "7805", 25, GREEN, 700), txt(291, 354, "IN  GND  OUT", 16),
      path("M175 311 L272 311", BLUE), txt(194, 296, "+24 V", 16, BLUE, 700),
      path("M175 341 L233 341 L233 366 L272 366", GRAY), txt(180, 395, "GND return", 16, GRAY),
      path("M462 320 L522 320", GREEN), txt(464, 304, "+5 V net", 17, GREEN, 700),

      rect(302, 432, 122, 63, "white", "#cbd8e3", 4),
      txt(317, 457, "C1  1 uF", 16, BLUE, 700), txt(313, 480, "IN to GND", 14),

      rect(302, 505, 122, 60, "white", "#cbd8e3", 4),
      txt(308, 530, "C2  0.1 uF", 16, GREEN, 700), txt(308, 551, "OUT to GND", 14),
      txt(65, 606, "Rail diode: reported present; type/orientation not verified.", 15, ORANGE)]

# Nano.
p += [rect(592, 220, 373, 737, "#eaf2fb", BLUE, 17),
      txt(617, 260, "ARDUINO NANO", 27, NAVY, 700),
      txt(620, 293, "ATmega328P   |   5 V logic", 18, GRAY),
      txt(619, 336, "5V  ←  7805 OUT", 21, GREEN, 700),
      txt(619, 378, "GND  ←  common ground", 19, GRAY),
      txt(619, 430, "D2  ←  sensor 1 OUT", 20, BLUE, 700),
      txt(619, 482, "D3  ←  sensor 2 OUT", 20, BLUE, 700),
      txt(619, 555, "D4  reserved; unused", 18, GRAY),
      txt(619, 675, "D5  →  pump gate", 21, NAVY, 700),
      txt(619, 755, "D6  →  valve 1 gate", 21, NAVY, 700),
      txt(619, 835, "D7  →  valve 2 gate", 21, NAVY, 700),
      txt(619, 913, "USB and 7805: isolate supplies for upload.", 15, ORANGE)]

# Sensors on left lower half. Named nets feed Nano; power rails are labelled.
for y, idx, pin in [(666, 1, "D2"), (839, 2, "D3")]:
    p += [rect(42, y, 509, 149), txt(62, y + 37, f"E18-D80NK  |  SENSOR {idx}", 21, NAVY, 700),
          txt(63, y + 70, "VCC  →  +5 V    GND  →  GND", 18),
          txt(63, y + 105, f"OUT  →  Nano {pin}    (active LOW)", 18, BLUE, 700),
          txt(63, y + 130, "NPN open collector; Nano INPUT_PULLUP", 15, GRAY)]

# Three identical output panels with a real supply/load/drain/source/gate topology.
labels = [("PUMP", "D5", "R1", "Q1", "R4", 0),
          ("VALVE 1", "D6", "R2", "Q2", "R5", 1),
          ("VALVE 2", "D7", "R3", "Q3", "R6", 2)]
for title, gpio, rs, q, rp, i in labels:
    y = 218 + i * 245
    p += [rect(997, y, 778, 232),
          txt(1020, y + 34, title + "  |  " + gpio, 22, NAVY, 700),
          txt(1020, y + 69, "+24 V", 17, BLUE, 700),
          line(1085, y+63, 1128, y+63, BLUE),
          rect(1128, y+43, 172, 42, "#eaf2fb", BLUE, 5),
          txt(1214, y+71, "24 V LOAD", 16, BLUE, 700, "middle"),
          line(1300, y+63, 1522, y+63, BLUE),
          line(1522, y+63, 1522, y+132, BLUE),
          node(1522, y+102, BLUE),
          txt(1534, y+121, "DRAIN", 14, BLUE, 700),
          rect(1445, y+131, 154, 52, "#e9f7f2", GREEN, 7),
          txt(1522, y+162, q + "  IRLZ44N", 17, GREEN, 700, "middle"),
          line(1522, y+183, 1522, y+208, GRAY),
          line(1522, y+208, 1650, y+208, GRAY),
          txt(1658, y+213, "GND", 16, GRAY, 700),
          txt(1020, y+150, gpio, 18, NAVY, 700),
          line(1056, y+146, 1103, y+146),
          rect(1103, y+133, 126, 27, "white", INK, 2),
          txt(1166, y+152, rs+" 330 Ω", 14, INK, 700, "middle"),
          line(1229, y+146, 1445, y+146),
          node(1367, y+146),
          txt(1380, y+135, "GATE", 13, INK),
          line(1367, y+146, 1367, y+169),
          rect(1354, y+169, 27, 29, "white", INK, 1),
          txt(1307, y+191, rp+" 10k", 13, INK, 700, "end"),
          path(f"M1367 {y+198} L1367 {y+208} L1522 {y+208}", GRAY),
          # Dashed missing flyback diode. The arrows identify the two ends unequivocally.
          path(f"M1085 {y+63} L1085 {y+111} L1175 {y+111}", ORANGE, 2, "7 6"),
          rect(1175, y+95, 181, 32, "#fff5e8", ORANGE, 4, 2),
          txt(1265, y+116, "D?  K:+  A:drain", 13, ORANGE, 700, "middle"),
          path(f"M1356 {y+111} L1522 {y+111}", ORANGE, 2, "7 6")]
p += [rect(42, 1011, 1733, 106, "#eaf2fb", "#c9d9ea", 8, 1),
      txt(63, 1044, "IRLZ44N face toward you, leads downward: Gate  |  Drain  |  Source. Metal tab = Drain.", 19, NAVY, 700),
      txt(63, 1075, "Supply fuse and flyback parts are recommended; fuse placement/status not independently verified.", 17, GRAY),
      txt(63, 1099, "Output wires are power wiring. Keep load return out of the Nano/sensor ground path.", 15, GRAY)]
(OUT / "schematic.svg").write_text(svg(1810, 1145, p), encoding="utf-8")

b = [txt(48, 60, "OBERON MIST  |  board wiring map", 33, NAVY, 700),
     txt(49, 93, "Connections by function. Physical connector order other than supply is not asserted.", 17, GRAY),
     rect(35, 117, 1445, 66, "#fff5e8", "#edc89c", 8, 1),
     txt(54, 158, "Power OFF before moving wires. Load flyback diodes have not been installed on this build.", 19, ORANGE, 700),
     rect(44, 225, 392, 545, "#eaf2fb", BLUE),
     txt(67, 267, "NANO 5 V", 28, NAVY, 700)]
pin_data=[("5V", "+5 V from 7805 OUT"), ("GND", "common GND"), ("D2", "sensor 1 OUT"), ("D3", "sensor 2 OUT"),
          ("D5", "330 Ω → pump Gate"), ("D6", "330 Ω → valve 1 Gate"), ("D7", "330 Ω → valve 2 Gate")]
for i, (pin, dst) in enumerate(pin_data):
    yy=317+i*60
    b += [rect(66, yy-26, 85, 37, "white", BLUE, 4), txt(108, yy, pin, 18, BLUE, 700, "middle"),
          line(151, yy-7, 195, yy-7, BLUE), txt(209, yy, dst, 17, INK)]
b += [rect(465, 225, 515, 545),
      txt(488, 266, "POWER + SENSORS", 24, NAVY, 700),
      txt(489, 324, "24 V + → 7805 IN + load positive", 19, BLUE),
      txt(489, 370, "24 V − → common GND", 19, GRAY),
      txt(489, 416, "7805 OUT → Nano 5V + sensors VCC", 19, GREEN),
      txt(489, 462, "Sensor 1 OUT → D2  |  Sensor 2 OUT → D3", 18),
      txt(489, 518, "C1: 1 uF  IN to GND", 18),
      txt(489, 557, "C2: 0.1 uF  OUT to GND", 18),
      txt(489, 608, "E18-D80NK: active LOW", 18, BLUE, 700),
      txt(489, 647, "VIN: not connected", 19, ORANGE, 700),
      txt(489, 693, "D4: reserved, not implemented", 17, GRAY)]
b += [rect(1006, 225, 470, 545),
      txt(1029, 266, "3 LOAD CHANNELS", 24, NAVY, 700)]
for i, (name, pin, _, _, _, _) in enumerate(labels):
    yy=317+i*128
    b += [txt(1033, yy, name, 21, BLUE, 700),
          txt(1033, yy+37, "Load + → 24 V   |   Load − → Drain", 17),
          txt(1033, yy+66, "Gate → 330 Ω → "+pin, 17),
          txt(1033, yy+94, "Source → GND   |   Gate → 10k → Source", 15)]
b += [rect(44, 807, 1432, 111, "#e9f7f2", GREEN),
      txt(65, 843, "Across EACH load: add properly rated flyback protection; diode K at +24 V and A at Drain.", 20, GREEN, 700),
      txt(65, 878, "The supplied rail diode does not replace load clamps. Check 7805 temperature at 24 V input.", 18, GRAY)]
(OUT / "board-wiring.svg").write_text(svg(1520, 948, b), encoding="utf-8")
print("Rendered schematic.svg and board-wiring.svg")

