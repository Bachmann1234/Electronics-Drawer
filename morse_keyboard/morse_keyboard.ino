#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <HID.h>
#include <Mouse.h>
#include <Keyboard.h>
#include <Wire.h>

#define DEBUG 0


// Screen config
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET     -1
#define SCREEN_ADDRESS 0x3C
#define TEXT_SIZE 10

// Key config
#define KEY_DOWN 1
#define KEY_UP 0
#define KEY_DOWN_THRESHOLD 1000
#define KEY_PIN A0
#define DOT_LENGTH_MS 100
#define DASH_LENGTH_MS DOT_LENGTH_MS * 3

// Code Entered
#define NO_CODE 0
#define DOT 1
#define DASH 2

// Key State
int keyState = KEY_UP;
int lastState = KEY_UP;
long timeDown = 0;
int lastCodeEntered = NO_CODE;
int writeCodeToKeyboard = 0;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  if (DEBUG) {
    Serial.begin(9600);
  }
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Don't proceed, loop forever
  }
  Keyboard.begin();
}

void loop() {
  readKeyState();
  drawScreen();
  handleKeyboardInput();
  lastState = keyState;
}

void readKeyState() {
  int currentState = isKeyDown();
  if (lastState == KEY_UP && currentState == KEY_DOWN) {
    timeDown = millis();
  }
  if (lastState == KEY_DOWN && currentState == KEY_UP) {
    lastCodeEntered = enteredCode(millis() - timeDown);
    writeCodeToKeyboard = 1;
  }

  lastState = keyState;
  keyState = currentState;
}

int isKeyDown() {
  int sensorValue = analogRead(KEY_PIN);
  if (DEBUG) {
    Serial.println(sensorValue);
  }
  if (sensorValue < KEY_DOWN_THRESHOLD) {
    return KEY_DOWN;
  }
  return KEY_UP;
}

int enteredCode(long totalTimeDown) {
  if (totalTimeDown < DASH_LENGTH_MS) {
    return DOT;
  }
  return DASH;
}

void drawScreen() {
  display.clearDisplay();
  display.setTextSize(TEXT_SIZE);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(lastCodeEntered == DOT ? 25 : 30, -20);
  if (lastCodeEntered) {
    display.println(lastCodeEntered == DOT ? "." : "_");
  }
  display.display();
}

void handleKeyboardInput() {
  if(writeCodeToKeyboard) {
    Keyboard.write(lastCodeEntered == DOT ? '.' : '-');
    writeCodeToKeyboard = 0;
  }
}
