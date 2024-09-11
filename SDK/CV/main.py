import cv2
import serial
import numpy as np


class ObjectTracker():
    camera_stream_path: int
    serial_path: str
    ser = None
    cap = None
    cap_frame = None
    proc_frame = None

    def __init__(self, camera_stream_path = 1, serial_path = ""):
        self.camera_stream_path = camera_stream_path
        self.serial_path = serial_path

    def openSerial(self):
        self.ser = serial.Serial(self.serial_path, 115200)
    
    def closeSerial(self):
        self.ser.close()
    
    def sendSerial(self, msg: str):
        if self.ser.is_open:
            self.ser.write(msg)
    
    def openStream(self):
        self.cap = cv2.VideoCapture(self.camera_stream_path)
        if not (self.cap.isOpened()):
            print("Could not open video device")
            exit()

    def readStream(self):
        ret, self.cap_frame = self.cap.read()
        h, w, _ = self.cap_frame.shape
        self.mid_h = int(h/2)
        self.mid_w = int(w/2)
    
    def showStream(self, frame):
        cv2.imshow("frame", frame)
    
    def closeStream(self):
        cv2.destroyAllWindows()
        self.cap.release()
    
    def run(self):
        self.openStream()
        # self.openSerial()
        while 1:
            self.readStream()

            self.track()
            self.process_frame()
            self.showStream(self.proc_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.closeStream()
                # self.closeSerial()
                break
    
    def process_frame(self):

        # flip frame
        self.cap_frame = cv2.flip(self.cap_frame, 1)

        self.proc_frame = cv2.circle(self.cap_frame, (self.mid_w, self.mid_h), 1, (255,0,255), 3)

        self.proc_frame = cv2.line(self.proc_frame, (self.mid_w, self.mid_h), (self.x_req, self.y_req), (255,0,0), 3)
        
        # self.proc_frame = cv2.putText(self.proc_frame,'words',(10,500), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),2, cv2.LINE_AA)
        # self.proc_frame = cv2.circle(self.proc_frame, (self.x_req, self.y_req), 10, (255,0,255), 5)
        # self.proc_frame = cv2.rectangle(self.proc_frame, (self.mid_w-50, self.mid_h-50), (self.mid_w+50, self.mid_h+50), (255, 255, 0), 3)
        # self.proc_frame = cv2.rectangle(self.cap_frame, (self.mid_w-50, self.mid_h-50), (self.mid_w+50, self.mid_h+50), (255, 255, 0), 1)
    
    def getObjectLocationOnFrame(self):
        return 250, 250

    def calcOffsetFromCenterOfFrame(self, x, y):
        return (self.mid_w-x), (self.mid_h-x)

    def track(self):
        x, y = self.getObjectLocationOnFrame()
        self.x_req, self.y_req = self.calcOffsetFromCenterOfFrame(x, y)
    
    def sendTrackingReq(self):
        req_str = f"x{self.x_req} y{self.y_req}"
        self.sendSerial(req_str)

def main():
    objectTracker = ObjectTracker(1, "/dev/ttyUSB0")
    objectTracker.run()


if __name__ == "__main__":
    main()
