#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <HX711.h>

// Coded up for:
// Feather 328p
// Adafruit FeatherWing OLED
// HX711 scale

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_RESET     -1 
#define SCREEN_ADDRESS 0x3C
#define BUTTON_PIN 3
#define SCALE_DATA_PIN 4
#define SCALE_CLOCK_PIN 5
#define VBATPIN A6
#define SCALE_CALIBRATION_SCALE 487.9
#define SCALE_CALIBRATION_OFFSET 105912
#define OZ_IN_GRAM 0.0353

HX711 scale;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int buttonVal = LOW;
int lastButtonVal = LOW;

void initScale() {
  scale.begin(SCALE_DATA_PIN, SCALE_CLOCK_PIN);
  scale.set_scale(SCALE_CALIBRATION_SCALE);
  scale.set_offset(SCALE_CALIBRATION_OFFSET);
  scale.tare(10);
}

void setup() {
  pinMode(BUTTON_PIN, INPUT);
  Serial.begin(9600);

  initScale();

  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

}

void loop() {
  checkTare();
  float oz = scaleReadinginOz();
  float battery = getBatteryPercent();
  drawReadings(oz, battery);
  delay(10);
  yield();
}

void checkTare() {
  buttonVal = digitalRead(BUTTON_PIN);
  if (buttonVal == HIGH && lastButtonVal == LOW) {
    scale.tare(10);
  }
  lastButtonVal = buttonVal;
}

float getBatteryPercent() {
  https://learn.adafruit.com/adafruit-feather-328p-atmega328-atmega328p/power-management
  float measuredvbat = analogRead(VBATPIN);
  measuredvbat *= 2;    // we divided by 2, so multiply back
  measuredvbat *= 3.3;  // Multiply by 3.3V, our reference voltage
  measuredvbat /= 1024; // convert to voltage
  
  return measuredvbat - 3.2; // Max bat 4.2, min bat 3.2 (denominator simplifies to 1) 
}

float scaleReadinginOz() {
  float grams = round(scale.get_units(2));
  return grams * OZ_IN_GRAM;
}


void drawReadings(float oz, float battery) {
  int textSize = oz < 100 ? 3 : 2;
  if(oz < .01 && oz > .01) {
    oz = 0;
  }
  display.clearDisplay();
  display.setTextSize(textSize);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(12, 10);
  display.print(oz, 2);
  if (battery < .1) {
    display.print("l");
  }
  display.display();
}
