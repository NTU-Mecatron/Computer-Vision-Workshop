/**
 * @file main.cpp
 * @author Scott CJX (scottcjx.w@gmail.com)
 * @brief 
 * @version 0.1
 * @date 2024-09-14
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#include <Arduino.h>
#include <Servo.h>

#define servoXPin 9
#define servoYPin 10

Servo servoX;
Servo servoY;

// Variables to store the received x and y coordinates
int x_req = 0;
int y_req = 0;

// Function to parse the incoming data and set servo positions
void processSerialData(String data) {
    int xIndex = data.indexOf('x') + 1;
    int yIndex = data.indexOf('y') + 1;

    if (xIndex != -1 && yIndex != -1) {
        char xSign = data.charAt(xIndex);
        char ySign = data.charAt(yIndex);

        // Define default angles for positive, negative, and zero
        int xAngle = 90; // Neutral position
        int yAngle = 90; // Neutral position

        // Map signs to servo angles
        if (xSign == '+') {
            xAngle = 180; // Maximum position
        } else if (xSign == '-') {
            xAngle = 0;   // Minimum position
        }
        
        if (ySign == '+') {
            yAngle = 180; // Maximum position
        } else if (ySign == '-') {
            yAngle = 0;   // Minimum position
        }
        
        // Move the servos to the desired positions
        servoX.write(xAngle);
        servoY.write(yAngle);
    }
}

void setup() {
    Serial.begin(115200);
    
    // Attach the servo motors to their pins
    servoX.attach(servoXPin);
    servoY.attach(servoYPin);
}

void loop() {
    if (Serial.available() > 0) {
        String incomingData = Serial.readStringUntil('\n');
        processSerialData(incomingData);
    }
}
