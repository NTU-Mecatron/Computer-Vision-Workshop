# Object Tracking System

This project is an object tracking system that uses a YOLO (You Only Look Once) model to detect objects in a video stream and tracks their position relative to the center of the frame. It sends tracking data via serial communication.

## Dependencies

- `cv2` (OpenCV)
- `torch`
- `ultralytics`
- `serial`

## Installation

Install the required Python packages using pip:

- for mac/ linux
    - `sh scripts/installation.sh`
- for windows 
    - run `installation.bat` in `scripts` folder

## Code Overview

### Classes

#### `CVModel`

Handles the YOLO model for object detection.

- **Constructor**: `__init__(self, yolo_model_name)`
  - `yolo_model_name`: Path to the YOLO model file.

- **Methods**:
  - `set_model(self)`: Loads the YOLO model.
  - `predict(self, frame)`: Predicts objects in the given frame.
  - `inference_locations(self)`: Processes detection results and stores object locations.

#### `CvVisualizer`

Manages video stream capture and display.

- **Constructor**: `__init__(self, camera_stream_path)`
  - `camera_stream_path`: Path or ID of the video capture device.

- **Methods**:
  - `readStream(self)`: Reads a frame from the video stream.
  - `get_frame_details(self)`: Retrieves frame dimensions and calculates the frame center.
  - `showStream(self, frame)`: Displays the frame in a window.
  - `closeStream(self)`: Closes the video stream and destroys the window.

#### `SerialComms`

Handles serial communication for sending tracking data.

- **Constructor**: `__init__(self, serial_path, baud_rate=115200)`
  - `serial_path`: Path to the serial port.
  - `baud_rate`: Serial communication speed.

- **Methods**:
  - `openSerial(self)`: Opens the serial port.
  - `closeSerial(self)`: Closes the serial port.
  - `sendSerial(self, msg: str)`: Sends a message via the serial port.

#### `ObjectTracker`

Coordinates object detection, tracking, and serial communication.

- **Constructor**: `__init__(self)`
  - Initializes attributes for object tracking.

- **Methods**:
  - `set_cvmodel(self, cvmodel: CVModel)`: Sets the `CVModel` instance.
  - `set_cvvisualizer(self, cvvisualizer: CvVisualizer)`: Sets the `CvVisualizer` instance and updates frame dimensions.
  - `openStream(self)`: Opens the video stream and retrieves frame details.
  - `closeStream(self)`: Closes the video stream and serial communication.
  - `run(self)`: Main loop for reading frames, predicting objects, tracking, and displaying results.
  - `process_frame(self)`: Processes the frame, draws bounding boxes and tracking lines.
  - `getObjectLocationOnFrame(self)`: Retrieves the location of the first detected object.
  - `calcOffsetFromCenterOfFrame(self, x, y)`: Calculates the offset of the object from the frame center.
  - `track(self)`: Tracks the object and sends tracking data.
  - `sendTrackingReq(self)`: Sends tracking data via serial communication.

### Main Function

- **Function**: `main()`
  - Initializes and sets up the `CVModel`, `CvVisualizer`, `ObjectTracker`, and `SerialComms` instances.
  - Starts the object tracking process.

## Usage

1. Ensure your serial device is connected and configured properly.
2. Update paths in the `main()` function for the YOLO model and serial port as needed.
3. Run the script:

```bash
python3 main.py
```

4. The application will open a window displaying the video stream with detected objects and their tracking lines. Press 'q' to exit.

## Notes

- Adjust the `camera_stream_path` and YOLO model path in the `main()` function as per your setup.
- The object detection model and serial port configuration might need to be modified based on your hardware and environment.

