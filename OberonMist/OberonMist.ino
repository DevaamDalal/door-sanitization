/*
  Oberon Mist — two-door controller
  Arduino Nano ATmega328P, 5 V / 16 MHz
  E18-D80NK sensors: active LOW / NPN open collector on D2 and D3.
  MOSFET gates: active HIGH on D5 (pump), D6 (valve 1), D7 (valve 2).
  D4 is reserved, and no tank-level shutdown is implemented.
  Each load requires its own suitable flyback clamp; see docs/wiring.md.
*/

#include <Arduino.h>

const byte SENSOR_1 = 2;
const byte SENSOR_2 = 3;
const byte PUMP     = 5;
const byte VALVE_1  = 6;
const byte VALVE_2  = 7;

const unsigned long FILTER_MS   = 40;
const unsigned long CLEAR_MS    = 200;
const unsigned long SPRAY_MS    = 1000;
const unsigned long COOLDOWN_MS = 4000;

enum State { WAIT_CLEAR, ARMED, SPRAYING, COOLDOWN };

struct Door {
  byte sensorPin;
  byte valvePin;
  State state;
  bool rawReading;
  bool stableReading;
  unsigned long rawChangedAt;
  unsigned long clearSince;
  unsigned long stateStartedAt;
};

Door doors[2] = {
  { SENSOR_1, VALVE_1, WAIT_CLEAR, HIGH, HIGH, 0, 0, 0 },
  { SENSOR_2, VALVE_2, WAIT_CLEAR, HIGH, HIGH, 0, 0, 0 }
};

void updateDoor(Door &door, unsigned long now) {
  bool reading = digitalRead(door.sensorPin);

  if (reading != door.rawReading) {
    door.rawReading = reading;
    door.rawChangedAt = now;
  }

  if (reading != door.stableReading &&
      now - door.rawChangedAt >= FILTER_MS) {
    door.stableReading = reading;
    door.clearSince = now;
  }

  switch (door.state) {
    case WAIT_CLEAR:
      if (door.stableReading == HIGH &&
          now - door.clearSince >= CLEAR_MS) {
        door.state = ARMED;
      }
      break;

    case ARMED:
      if (door.stableReading == LOW) {
        door.state = SPRAYING;
        door.stateStartedAt = now;
      }
      break;

    case SPRAYING:
      if (now - door.stateStartedAt >= SPRAY_MS) {
        door.state = COOLDOWN;
        door.stateStartedAt = now;
      }
      break;

    case COOLDOWN:
      if (now - door.stateStartedAt >= COOLDOWN_MS) {
        door.state = WAIT_CLEAR;
        door.clearSince = now;
      }
      break;
  }
}

void setup() {
  digitalWrite(PUMP, LOW);
  digitalWrite(VALVE_1, LOW);
  digitalWrite(VALVE_2, LOW);

  pinMode(PUMP, OUTPUT);
  pinMode(VALVE_1, OUTPUT);
  pinMode(VALVE_2, OUTPUT);

  pinMode(SENSOR_1, INPUT_PULLUP);
  pinMode(SENSOR_2, INPUT_PULLUP);

  unsigned long now = millis();
  for (byte i = 0; i < 2; i++) {
    doors[i].rawReading = digitalRead(doors[i].sensorPin);
    doors[i].stableReading = doors[i].rawReading;
    doors[i].rawChangedAt = now;
    doors[i].clearSince = now;
    doors[i].stateStartedAt = now;
  }
}

void loop() {
  unsigned long now = millis();

  updateDoor(doors[0], now);
  updateDoor(doors[1], now);

  bool spraying1 = doors[0].state == SPRAYING;
  bool spraying2 = doors[1].state == SPRAYING;

  digitalWrite(VALVE_1, spraying1 ? HIGH : LOW);
  digitalWrite(VALVE_2, spraying2 ? HIGH : LOW);
  digitalWrite(PUMP, (spraying1 || spraying2) ? HIGH : LOW);
}
