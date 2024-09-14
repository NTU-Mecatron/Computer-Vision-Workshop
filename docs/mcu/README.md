# Arduino Servo Control

This project demonstrates how to control two servo motors using an Arduino based on serial commands. The commands are sent via serial communication and indicate the position of the motors relative to a center point.

## Dependencies

- Arduino IDE
- Servo library (included with the Arduino IDE)

## Code Overview

### Pin Definitions

- **servoXPin**: Pin connected to the X-axis servo motor.
- **servoYPin**: Pin connected to the Y-axis servo motor.

### Global Variables

- `int x_req`: Stores the requested X-axis position.
- `int y_req`: Stores the requested Y-axis position.

### Functions

#### `void processSerialData(String data)`

Processes the incoming serial data and controls the servo motors based on the parsed commands.

- **Parameters**: 
  - `String data`: The serial data string received.
- **Functionality**:
  - Parses the `x` and `y` values from the data string.
  - Determines the servo angle based on the sign (`+`, `-`, `0`) associated with `x` and `y`.
  - Moves the servos to the computed angles.

#### `void setup()`

Initializes serial communication and attaches the servo motors to their respective pins.

- **Functionality**:
  - Starts serial communication at `115200` baud.
  - Attaches servos to the defined pins.

#### `void loop()`

Continuously checks for incoming serial data and processes it.

- **Functionality**:
  - Reads incoming serial data until a newline character is encountered.
  - Calls `processSerialData()` to handle the received data.

## Code

```cpp
/**
 * @file main.cpp
 * @author Scott CJX (scottcjx.w@gmail.com)
 * @brief Controls two servos based on serial input data.
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
```

## Usage

1. **Connect** the servo motors to the defined pins on the Arduino (Pin 9 for X-axis and Pin 10 for Y-axis).
2. **Upload** the code to the Arduino using the Arduino IDE.
3. **Send Serial Commands**: Use a serial terminal or another device to send commands in the format `x<sign> y<sign>`, where `<sign>` can be `+`, `-`, or `0`.

   Example Commands:
   - `x+ y-` : Move X-axis servo to 180 degrees and Y-axis servo to 0 degrees.
   - `x- y0` : Move X-axis servo to 0 degrees and Y-axis servo to 90 degrees.

4. The servo motors will move according to the received commands.

## Notes

- Ensure the servo motors are powered properly. The Arduino alone might not provide enough power for servos.
- Adjust servo angles and pin definitions as needed based on your specific setup and servo specifications.
- The serial baud rate in the Arduino code (`115200`) should match the baud rate used by your serial communication setup.
