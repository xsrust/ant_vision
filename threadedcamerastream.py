from threading import Thread
import cv2

# Threading the correct choice here because this operation is IO Blocked
class ThreadedCameraStream:
    def __init__(self, src=0):
        # init capture
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FPS, 500)
        # read first frame from stream
        _, self.frame = self.stream.read()
        # indicates thread should be stopped
        self.terminated = False
        # Functions as a pairity bit
        self.new = True

    """ Begin Reading from the camarea in a seperate Thread """
    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    """ Check for termination, if not terminated, read from camera """
    def update(self):
        while True:
            if self.terminated:
                return
            _, self.frame = self.stream.read()
            self.new =  not(self.new)

    """ Returns the last read image, and the pairity bit """
    def read(self):
        # return most recently read frame
        return self.frame, self.new

    """ Terminate the Threaded reading of the camera """
    def stop(self):
        self.terminated = True
