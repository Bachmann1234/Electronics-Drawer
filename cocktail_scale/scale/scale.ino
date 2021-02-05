#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <HX711.h>


#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET     -1 
#define SCREEN_ADDRESS 0x3C
#define BUTTON_PIN 7
#define SCALE_DATA_PIN 2
#define SCALE_CLOCK_PIN 3
#define SCALE_CALIBRATION_SCALE 454.78
#define SCALE_CALIBRATION_OFFSET 4000
#define OZ_IN_GRAM 0.0353

HX711 scale;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int buttonVal = LOW;
int lastButtonVal = LOW;

void initScale() {
  scale.begin(SCALE_DATA_PIN, SCALE_CLOCK_PIN);
  scale.tare();
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
  
  scale.tare();

}

void loop() {
  buttonVal = digitalRead(BUTTON_PIN);
  if (buttonVal == HIGH && lastButtonVal == LOW) {
    scale.tare();
  }
  lastButtonVal = buttonVal;
  float grams = round(scale.get_units(10));
  drawReading(grams * OZ_IN_GRAM);
}



void drawReading(float oz) {
  int textSize = oz < 100 ? 3 : 2;
  if(oz < .01 && oz > .01) {
    oz = 0;
  }
  display.clearDisplay();
  display.setTextSize(textSize);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(24, 20);
  display.println(oz, 2);
  display.display();
}
