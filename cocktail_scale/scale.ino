#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <HX711.h>


#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_RESET     -1 
#define SCREEN_ADDRESS 0x3C
#define BUTTON_PIN 7
#define SCALE_DATA_PIN 4
#define SCALE_CLOCK_PIN 5
#define SCALE_CALIBRATION_SCALE 487.9
#define SCALE_CALIBRATION_OFFSET 105912
#define OZ_IN_GRAM 0.0353

HX711 scale;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int buttonVal = LOW;
int lastButtonVal = LOW;

void initScale() {
  scale.begin(SCALE_DATA_PIN, SCALE_CLOCK_PIN);
  scale.tare(10);
  scale.set_scale(SCALE_CALIBRATION_SCALE);
  scale.set_offset(SCALE_CALIBRATION_OFFSET);
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
  buttonVal = digitalRead(BUTTON_PIN);
  if (buttonVal == HIGH && lastButtonVal == LOW) {
    scale.tare(10);
  }
  lastButtonVal = buttonVal;
  float grams = round(scale.get_units(2));
  drawReading(grams * OZ_IN_GRAM);
  delay(10);
  yield();
}



void drawReading(float oz) {
  int textSize = oz < 100 ? 3 : 2;
  if(oz < .01 && oz > .01) {
    oz = 0;
  }
  display.clearDisplay();
  display.setTextSize(textSize);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(12, 10);
  display.println(oz, 2);
  display.display();
}
