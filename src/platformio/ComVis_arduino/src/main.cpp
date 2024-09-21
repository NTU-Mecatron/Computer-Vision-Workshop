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
// Global variables to keep track of current servo angles
int currentXAngle = 90; // Start at neutral position
int currentYAngle = 90; // Start at neutral position

// Define step sizes
const int x_step = 2; // Step size for x-axis
const int y_step = 2; // Step size for y-axis

// Function to parse the incoming data and set servo positions
void processSerialData(String data) {
    int xIndex = data.indexOf('x') + 1;
    int yIndex = data.indexOf('y') + 1;

    if (xIndex != -1 && yIndex != -1) {
        char xSign = data.charAt(xIndex);
        char ySign = data.charAt(yIndex);

        // Update the x angle based on the sign
        if (xSign == '+') {
            currentXAngle += x_step;
            if (currentXAngle > 180) {
                currentXAngle = 180; // Limit to max angle
            }
        } else if (xSign == '-') {
            currentXAngle -= x_step;
            if (currentXAngle < 0) {
                currentXAngle = 0; // Limit to min angle
            }
        }
        
        // Update the y angle based on the sign
        if (ySign == '+') {
            currentYAngle += y_step;
            if (currentYAngle > 180) {
                currentYAngle = 180; // Limit to max angle
            }
        } else if (ySign == '-') {
            currentYAngle -= y_step;
            if (currentYAngle < 0) {
                currentYAngle = 0; // Limit to min angle
            }
        }
        
        // Move the servos to the updated positions
        servoX.write(currentXAngle);
        servoY.write(currentYAngle);
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
