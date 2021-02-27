#define TRIG_PIN 13
#define ECHO_PIN 12
#define PAUSE_PIN 6
#define SIT_LED_PIN A1
#define STAND_LED_PIN A2
#define SITTING_THRESHOLD_CM  80
#define SPEED_OF_SOUND_CM_MICROSEC 29.1
#define SIT_DISPLAY_ADDRESS 0x71
#define STAND_DISPLAY_ADDRESS 0x70
#define DEBOUNCE_DELAY 1000
#define DEBUG false

#include  "RTClib.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

Adafruit_7segment sitMatrix = Adafruit_7segment();
Adafruit_7segment standMatrix = Adafruit_7segment();

RTC_DS3231 rtc;
long startTime;
long runningTime;
long sitTime;
long standTime;
long lastDebounceTime = 0;

boolean isPaused = false;

enum SitState {
  INVALID, // sonar sensor reporting out of range
  SITTING,
  STANDING
};

void setup() {
  Serial.begin (9600);
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    abort();
  }
  if (rtc.lostPower()) {
    Serial.println("RTC lost power, let's set the time!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  pinMode(SIT_LED_PIN, OUTPUT);
  pinMode(STAND_LED_PIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(PAUSE_PIN, INPUT);
  digitalWrite(PAUSE_PIN, HIGH);
  sitMatrix.begin(SIT_DISPLAY_ADDRESS);
  standMatrix.begin(STAND_DISPLAY_ADDRESS);
  startTime = rtc.now().unixtime();
  sitTime = 0;
  standTime = 0;
  runningTime = 0;
}

long readDistance() {
  long duration, distance;
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN, HIGH);
  // converting the time to hit the ceiling
  // but divide by 2 since we are timing
  // hitting the ceiling and returning
  distance = (duration / 2) / SPEED_OF_SOUND_CM_MICROSEC;
  if (DEBUG) {
    Serial.print(distance);
    Serial.println(" cm");
  }
  return distance;
}

SitState getSitState() {
  long distance = readDistance();
  if (distance >= 200 || distance <= 0) {
    if (DEBUG) {
      Serial.println("Out of range");
    }
    return INVALID;
  }
  if (distance < SITTING_THRESHOLD_CM) {
    return SITTING;
  } else {
    return STANDING;
  }
}

long updateRunningTime() {
  long currentTime = rtc.now().unixtime();
  long currentRunningTime = currentTime - startTime;
  long secondsPassed = currentRunningTime - runningTime;
  runningTime = currentRunningTime;
  if (DEBUG) {
    Serial.print("Running Time: ");
    Serial.println(runningTime);
    Serial.print("Seconds Passed: ");
    Serial.println(secondsPassed);
  }
  return secondsPassed;
}

boolean updateTimers(boolean isSitting) {
  long secondsPassed = 0;
  secondsPassed = updateRunningTime();
  if (isPaused) {
    secondsPassed = 0;
  }
  if (isSitting) {
    if (DEBUG) {
      Serial.println("Sitting");
    }
    sitTime += secondsPassed;
  } else {
    if (DEBUG) {
      Serial.println("Standing");
    }
    standTime += secondsPassed;
  }
  return secondsPassed > 0;
}

void drawTimer(Adafruit_7segment display, long timerState) {
  long hours = timerState / 60 / 60;
  long minutes = timerState / 60 - (hours * 60);
  long seconds = timerState - (hours * 60 * 60) - (minutes * 60);
  if (DEBUG) {
    Serial.print(hours);
    Serial.print(":");
    Serial.print(minutes);
    Serial.print(":");
    Serial.print(seconds);
  }
  boolean drawDecinal = false;
  if (hours > 0) {
    display.drawColon(true);
    display.writeDigitNum(0, (hours / 10), drawDecinal);
    display.writeDigitNum(1, (hours % 10), drawDecinal);
    display.writeDigitNum(3, (minutes / 10), drawDecinal);
    display.writeDigitNum(4, (minutes % 10), drawDecinal);
  } else {
    display.writeDigitNum(0, (minutes / 10), drawDecinal);
    display.writeDigitNum(1, (minutes % 10), true);
    display.writeDigitNum(3, (seconds / 10), drawDecinal);
    display.writeDigitNum(4, (seconds % 10), drawDecinal);
  }
  display.writeDisplay();

}

void updatePauseState() {
  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY) {
    if (digitalRead(PAUSE_PIN) == LOW) {
      isPaused = !isPaused;
      if (DEBUG) {
        Serial.println("PAUSE HIT");
        Serial.print("isPaused: ");
        Serial.println(isPaused);
      }
      lastDebounceTime = millis();
    }
  }
}

void clearDisplay(Adafruit_7segment display) {
  display.clear();
  display.writeDisplay();
}

void updateLeds(SitState sitState) {
  if (sitState == SITTING) {
    digitalWrite(SIT_LED_PIN, HIGH);
    digitalWrite(STAND_LED_PIN, LOW);
  } else if (sitState == STANDING) {
    digitalWrite(SIT_LED_PIN, LOW);
    digitalWrite(STAND_LED_PIN, HIGH);
  } else {   
    digitalWrite(SIT_LED_PIN, LOW);
    digitalWrite(STAND_LED_PIN, LOW); 
  }
}

void loop() {
  updatePauseState();
  SitState sitState = getSitState();
  updateLeds(sitState);
  boolean secondsHavePassed = updateTimers(sitState == SITTING);
  if ((secondsHavePassed && !isPaused) || (isPaused && runningTime % 2 == 0)) {
    if (DEBUG) {
      Serial.print("Sit time: ");
    }
    drawTimer(sitMatrix, sitTime);
    if (DEBUG) {
      Serial.println();
      Serial.print("Stand time: ");
    }
    drawTimer(standMatrix, standTime);
    if (DEBUG) {
      Serial.println();
      Serial.println("****");
    }
  }
  if (isPaused && runningTime % 2 != 0) {
    // I do this by hand
    // I tried using the blinkrate function
    // but I want both dispalys to blink
    // at the same time
    clearDisplay(sitMatrix);
    clearDisplay(standMatrix);
  }
  // For reasons I do not fully understand
  // I need a small delay here for the clock to operate
  // properly. I think its related to the sonar sensor
  // I did not observe this need when using an uno
  // but do notice it with the feather
  delay(DEBUG ? 1000 : 100);
}
