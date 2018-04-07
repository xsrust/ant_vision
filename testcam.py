from threading import Thread
import cv2
from time import sleep

class TestCam:
    def __init__(self,filename,framerate,permute):
        self.permute=permute
        self.framerate=1/(framerate)
        self.new=True
        self.terminated=False
        self.img=cv2.imread(filename)
        self.frame=self.img
        self.transforation = {}

    def update(self):
        while True:
            if self.terminated:
                return
            if self.permute:
                self.transform()
            self.new = not(self.new)
            #TODO: wait for 1/framerate seconds
            sleep(self.framerate)

    def start(self):
        Thread(target=self.update,args=()).start()
        return self

    """ Returns the last read image, and the pairity bit """
    def read(self):
        # return most recently read frame
        return self.frame, self.new

    """ Terminate the Threaded reading of the camera """
    def stop(self):
        self.terminated = True

    def transform(self):
        return
