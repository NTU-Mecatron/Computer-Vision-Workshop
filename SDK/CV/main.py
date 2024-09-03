import cv2


class ObjectTracker():
    camera_stream_path = 1
    cap = None
    cap_frame = None

    def __init__(self, camera_stream_path = 1):
        self.camera_stream_path = camera_stream_path
    
    def openStream(self):
        self.cap = cv2.VideoCapture(self.camera_stream_path)
        if not (self.cap.isOpened()):
            print("Could not open video device")
            exit()

    def readStream(self):
        ret, self.cap_frame = self.cap.read()
        return ret
    
    def showStream(self):
        cv2.imshow("frame", self.cap_frame)
    
    def closeStream(self):
        cv2.destroyAllWindows()
        self.cap.release()
    
    def run(self):
        self.openStream()
        while 1:
            self.readStream()
            self.showStream()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def main():
    objectTracker = ObjectTracker()
    objectTracker.run()


if __name__ == "__main__":
    main()
