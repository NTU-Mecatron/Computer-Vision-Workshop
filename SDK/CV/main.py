import cv2
from matplotlib import pyplot as plt
import yaml


class ObjectTracker():
    camera_stream_path = 0
    cap = None
    cap_frame = None

    def __init__(self, camera_stream_path = 0):
        self.camera_stream_path = camera_stream_path
    
    def openStream(self):
        self.cap = cv2.VideoCapture(self.camera_stream_path)
        if not (self.cap.isOpened()):
            print("Could not open video device")
            exit()

    def readStream(self):
        ret, self.cap_frame = self.cap.read()
    
    def showStream(self):
        cv2.imshow(self.__name__, self.cap)
    
    def run(self):
        self.openStream()
        while 1:
            self.readStream()
            self.showStream()
            if(cv2.waitKey(0) == 'q'):
                cv2.destroyAllWindows()


def main():
    objectTracker = ObjectTracker()
    objectTracker.run()

