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
#define SCALE_CALIBRATION_SCALE 455.25
#define SCALE_CALIBRATION_OFFSET 4078
#define FLUID_OZ_IN_GRAM 0.033814

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


}

void loop() {
  buttonVal = digitalRead(BUTTON_PIN);
  if (buttonVal == HIGH && lastButtonVal == LOW) {
    scale.tare();
  }
  lastButtonVal = buttonVal;
  float grams = scale.get_units(10);
  if ( grams < 0 && grams > -.05) {
    grams = 0;
  }
  drawReading(grams);
}



void drawReading(float grams) {
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(24, 20);
  display.print(grams, 1);
  display.print("g");
  display.display();
}
