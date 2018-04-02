import cv2
import numpy as np
import queue

class AntDetector:
    def __init__(self,options):
        # init re-used vars for processing and pass to function
        self.thresh = options["greyscaleThreshold"]
        self.kernel_size_op = options["kernelOpen"]
        self.kernel_size_cl = options["kernelClose"]
        self.kernel_op = np.ones((self.kernel_size_op,self.kernel_size_op),np.uint8)
        self.kernel_cl = np.ones((self.kernel_size_cl,self.kernel_size_cl),np.uint8)

    """
    Launched in another process
    work_q and results_q are used to communicate with the main process to recieve
        images and pass back processed centers and directions
    Options is a hash with the below keys
    worker_num mainly used for debugging which process is doing work

    Reads from work_q to see if there are any images ready to be Processed
    If there are, calls the process function belwo, and puts the results on results_q
    """
    def work_and_report(self, work_q, result_q, worker_num):
        while True:
            try:
                # check if new item on queue
                img = work_q.get_nowait()
                print("GOT AN IMAGE {0}".format(worker_num))
                results = self.process(img)
                results.append(worker_num)
                result_q.put_nowait(results)
            except queue.Empty:     # if  get_nowait() called on empty queue
                continue

    """
    Image processing logic
    img is the image given from the webcam
    thresh is the threshhold value from Options
    op and cl are the kernels generated from the specified options.json
    returns an array with the centerx, centery, and the angle of the line in degrees
    """
    def process(self, img):
        results = []
        # Threshhold dark ant against white background
        im_gr = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _, img_bin = cv2.threshold(im_gr, self.thresh, 255, cv2.THRESH_BINARY_INV)
        # Transformations to clean up the image
        #   opening to remove external noise
        #   closings to remove internal noise
        im_open = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, self.kernel_op)
        im_close = cv2.morphologyEx(im_open, cv2.MORPH_CLOSE, self.kernel_cl)
        # Given a cleaned detection, we now fit a line to the ant and find it's center of mass
        ret = cv2.findContours(im_close,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        contours = ret[1]
        areas = [cv2.contourArea(c) for c in contours]
        index = np.argmax(areas)
        ant = contours[index]
        # Find center of mass
        M = cv2.moments(ant)
            #results["centerX"] = int(M["m10"] / M["m00"])
        results.append(int(M["m10"] / M["m00"]))
            #results["centerY"] = int(M["m01"] / M["m00"])
        results.append(int(M["m01"] / M["m00"]))
        # fit a line through the ant
        [vx,vy,x,y] = cv2.fitLine(ant,cv2.DIST_L2,0,0.01,0.01)
            #results["direction"] = np.rad2deg(np.arctan(vy/vx))
        results.append(np.rad2deg(np.arctan(vy/vx)))
        # NOTE: Direction is only colinear to the line, not necissarily facing the correct way,
        # need to compare to previous to determine direction (at the moment)
        return results
