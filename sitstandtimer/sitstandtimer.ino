#define trigPin 13
#define echoPin 12
#define pausePin 8
#define SITTING_THRESHOLD_CM  60
//#define SITTING_THRESHOLD_CM  10
#define SPEED_OF_SOUND_CM_MICROSEC 29.1
#define SIT_DISPLAY_ADDRESS 0x71
#define STAND_DISPLAY_ADDRESS 0x70
#define DEBUG false

#include "RTClib.h"
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
int buttonState = LOW;
long lastDebounceTime = 0;
long debounceDelay = 1000;

boolean isPaused = false;

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
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(pausePin, INPUT);
  sitMatrix.begin(SIT_DISPLAY_ADDRESS);
  standMatrix.begin(STAND_DISPLAY_ADDRESS);
  startTime = rtc.now().unixtime();
  sitTime = 0;
  standTime = 0;
  runningTime = 0;
}

long readDistance() {
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  // converting the time to hit the ceiling
  // but divide by 2 since we are timing
  // hitting the ceiling and returning
  distance = (duration / 2) / SPEED_OF_SOUND_CM_MICROSEC;
  return distance;
}

boolean isSitting(long distance) {
  return distance > SITTING_THRESHOLD_CM;
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

boolean updateTimers() {
  long distance = readDistance();
  long secondsPassed = 0;
  if (distance >= 200 || distance <= 0) {
    if (DEBUG) {
      Serial.println("Out of range");
    }
  } else {
    secondsPassed = updateRunningTime();
    if (isPaused) {
      secondsPassed = 0;
    }
    if (DEBUG) {
      Serial.print(distance);
      Serial.println(" cm");
    }
    if (isSitting(distance)) {
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
  display.drawColon(true);
  boolean drawDecinal = false;
  if (hours > 0) {
    display.writeDigitNum(0, (hours / 10), drawDecinal);
    display.writeDigitNum(1, (hours % 10), drawDecinal);
    display.writeDigitNum(3, (minutes / 10), drawDecinal);
    display.writeDigitNum(4, (minutes % 10), drawDecinal);
  } else {
    display.writeDigitNum(0, (minutes / 10), drawDecinal);
    display.writeDigitNum(1, (minutes % 10), drawDecinal);
    display.writeDigitNum(3, (seconds / 10), drawDecinal);
    display.writeDigitNum(4, (seconds % 10), drawDecinal);
  }
  display.writeDisplay();

}

void updatePauseState() {
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (digitalRead(pausePin) == HIGH) {
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

void loop() {
  updatePauseState();
  boolean secondsHavePassed = updateTimers();
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
    clearDisplay(sitMatrix);
    clearDisplay(standMatrix);
  }
}
