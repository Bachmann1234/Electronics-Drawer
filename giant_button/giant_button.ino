#include "Keyboard.h"

const int buttonPin = 4;
int previousButtonState = HIGH;
int counter = 0;

void setup() {
  pinMode(buttonPin, INPUT);
  Keyboard.begin();
}

void loop() {
  int buttonState = digitalRead(buttonPin);
  if ((buttonState != previousButtonState)
      && (buttonState == HIGH)) {
      Keyboard.print("git commit");
      delay(100);
      Keyboard.write(KEY_RETURN);
      delay(1000);
  }
  previousButtonState = buttonState;
}
