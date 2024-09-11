#!/usr/bin/python3
import cv2
import torch
import ultralytics
from torch.backends import cudnn
import serial


class CVModel:
    def __init__(self, yolo_model_name):
        self.yolo_model_name = yolo_model_name
        self.model = None
        self.results = None
        self.results_tensor = None

    def set_model(self):
        self.model = ultralytics.YOLO(self.yolo_model_name)
        cudnn.benchmark = True
    
    def predict(self, frame):
        self.results = self.model.predict(source=frame, conf=0.6, iou=0.5)[0]

    def inference_locations(self):
        if self.results is None:
            return
        
        boxes = self.results.boxes
        xywhn = boxes.xywhn  # A 2D tensor of shape (N, 4) where N is the number of detected objects
        conf = boxes.conf  # A 1D tensor of shape (N,) containing the confidence scores of the detected objects
        cls = boxes.cls  # A 1D tensor of shape (N,) containing the class labels of the detected objects

        conf = conf.reshape(-1, 1)
        cls = cls.reshape(-1, 1)
        self.results_tensor = torch.cat((xywhn, conf, cls), dim=1)


class CvVisualizer:
    def __init__(self, camera_stream_path):
        self.camera_stream_path = camera_stream_path
        self.cap = cv2.VideoCapture(self.camera_stream_path)
        self.cap_frame = None
        self.h = self.w = self.mid_h = self.mid_w = 0

    def readStream(self):
        ret, self.cap_frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from the camera stream")

    def get_frame_details(self):
        if self.cap_frame is None:
            raise RuntimeError("Frame not read")
        
        self.h, self.w, _ = self.cap_frame.shape
        self.mid_h = int(self.h / 2)
        self.mid_w = int(self.w / 2)

    def showStream(self, frame):
        cv2.imshow("frame", frame)
    
    def closeStream(self):
        cv2.destroyAllWindows()
        self.cap.release()


class SerialComms:
    def __init__(self, serial_path, baud_rate=115200):
        self.serial_path = serial_path
        self.baud_rate = baud_rate
        self.ser = None

    def openSerial(self):
        self.ser = serial.Serial(self.serial_path, self.baud_rate)
    
    def closeSerial(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
    
    def sendSerial(self, msg: str):
        if self.ser and self.ser.is_open:
            self.ser.write(msg.encode())


class ObjectTracker:
    def __init__(self):
        self.cvmodel = None
        self.cvvisualizer = None
        self.serial_comms = SerialComms("COM3")  # Adjust COM port as necessary
        self.cap_frame = None
        self.mid_w = self.mid_h = 0
        self.x_req = self.y_req = 0
        self.w = self.h = 0  # Add these attributes to store frame width and height

    def set_cvmodel(self, cvmodel: CVModel):
        self.cvmodel = cvmodel

    def set_cvvisualizer(self, cvvisualizer: CvVisualizer):
        self.cvvisualizer = cvvisualizer
        # Update width and height from cvvisualizer
        self.w = self.cvvisualizer.w
        self.h = self.cvvisualizer.h
        self.mid_w = self.cvvisualizer.mid_w
        self.mid_h = self.cvvisualizer.mid_h

    def openStream(self):
        if self.cvvisualizer:
            self.cvvisualizer.readStream()
            self.cvvisualizer.get_frame_details()
            # Update width and height from cvvisualizer after getting frame details
            self.w = self.cvvisualizer.w
            self.h = self.cvvisualizer.h
            self.mid_w = self.cvvisualizer.mid_w
            self.mid_h = self.cvvisualizer.mid_h

    def closeStream(self):
        if self.cvvisualizer:
            self.cvvisualizer.closeStream()
        if self.serial_comms:
            self.serial_comms.closeSerial()

    def run(self):
        self.openStream()
        while True:
            self.cvvisualizer.readStream()
            self.cvmodel.predict(self.cvvisualizer.cap_frame)
            self.cvmodel.inference_locations()
            self.track()
            self.process_frame()
            self.cvvisualizer.showStream(self.proc_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.closeStream()
                break

    def process_frame(self):
        if self.cvvisualizer.cap_frame is None:
            return

        # Flip frame
        # self.cap_frame = cv2.flip(self.cvvisualizer.cap_frame, 0)
        self.proc_frame = self.cap_frame = self.cvvisualizer.cap_frame
        
        # Draw bounding boxes
        if self.cvmodel.results_tensor is not None:
            for box in self.cvmodel.results_tensor:
                x_center, y_center, width, height, conf, cls = box
                x_center, y_center, width, height = x_center * self.w, y_center * self.h, width * self.w, height * self.h
                x1, y1 = int((x_center - width / 2)), int((y_center - height / 2))
                x2, y2 = int((x_center + width / 2)), int((y_center + height / 2))

                # Draw the bounding box
                color = (0, 255, 0)  # Green color for bounding box
                self.proc_frame = cv2.rectangle(self.proc_frame, (x1, y1), (x2, y2), color, 2)
                self.proc_frame = cv2.line(self.proc_frame, (self.mid_w, self.mid_h), (int((x1+x2)/2), int((y1+y2)/2)), (255, 0, 0), 3)

        self.proc_frame = cv2.flip(self.proc_frame, 1)

        # Draw center point and tracking line
        self.proc_frame = cv2.circle(self.proc_frame, (self.mid_w, self.mid_h), 1, (255, 0, 255), 3)
        

    def getObjectLocationOnFrame(self):
        # Placeholder for actual object location logic
        return 250, 250

    def calcOffsetFromCenterOfFrame(self, x, y):
        return (self.mid_w - x), (self.mid_h - y)

    def track(self):
        x, y = self.getObjectLocationOnFrame()
        self.x_req, self.y_req = self.calcOffsetFromCenterOfFrame(x, y)
        self.sendTrackingReq()

    def sendTrackingReq(self):
        req_str = f"x{self.x_req} y{self.y_req}\n"
        self.serial_comms.sendSerial(req_str)



def main():
    cvmodel = CVModel("SDK/CV/models/yolov8m-face.pt")
    cvmodel.set_model()

    cvvisualizer = CvVisualizer(1)  # Use 0 for default camera; adjust as necessary

    objectTracker = ObjectTracker()
    objectTracker.set_cvmodel(cvmodel)
    objectTracker.set_cvvisualizer(cvvisualizer)

    serial_path = "/dev/ttyUSB0"  # Adjust as necessary
    objectTracker.serial_comms = SerialComms(serial_path)
    # objectTracker.serial_comms.openSerial()

    objectTracker.run()


if __name__ == "__main__":
    main()
