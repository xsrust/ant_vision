from threading import Thread
import cv2
from time import sleep
import numpy as np
from random import randrange

class TestCam:
    def __init__(self,filename,framerate,permute,x=800,y=600):
        self.permute=permute
        self.framerate=1/(framerate)
        self.new=True
        self.terminated=False
        self.img=cv2.resize(cv2.imread(filename),(x,y),interpolation=cv2.INTER_CUBIC)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        self.frame = self.img
        self.transformations = []
        self.x = x
        self.y = y
        self.cx = x/2
        self.cy = y/2

    def set_center(self,cx,cy):
        self.cx = cx
        self.cy = cy


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
        return self.frame, self.new, self.transformations

    """ Terminate the Threaded reading of the camera """
    def stop(self):
        self.terminated = True

    def transform(self):
        # Here we want to rotate or translate the ant within the image
        tx = randrange(-25,25)
        ty = randrange(-25,25)
        rot = randrange(-89,89)
        M = np.float32([[1,0,tx],[0,1,ty]])
        f = cv2.warpAffine(self.img,M,(self.x,self.y),borderValue=255)
        R = cv2.getRotationMatrix2D((self.cx+tx,self.cy+ty),rot,1)
        self.frame = cv2.warpAffine(f,R,(self.x,self.y),borderValue=255)
        self.transformations = [tx,ty,rot]
