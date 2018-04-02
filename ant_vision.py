import cv2
import numpy as np
import time
import json
import multiprocessing as mp
import queue
from matplotlib import pyplot as plt
import threadedcamerastream as tcs
import antdetector

"""
Takes in the path to a json file with options
Begins reading from the specified webcam and processing images
"""
def start(options='options.json'):
    # initialize variables based on passed options
    json_dat = open(options)
    options = json.load(json_dat)
    num_workers = options["num_workers"]
    stream_no = options["cameraStream"]
    # create ThreadedCameraStream to read from
    stream = tcs.ThreadedCameraStream(stream_no)
    stream.start()
    # variable to compare to the flipped bit in ThreadedCameraStream
    last = False
    # create the Queue objects to communicate between processes
    work_q, result_q = mp.Queue(), mp.Queue()
    # Create processes to work off the queue
    processes = []
    ad = antdetector.AntDetector(options)
    #mp.set_start_method('spawn')
    for i in range(num_workers):
        processes.append(mp.Process(target=ad.work_and_report,args=(work_q,result_q,i)))
        # processes target work_and_report
        processes[-1].start()
    out_frames, proc_frames = 0,0
    time.sleep(2)
    starttime=None
    while True:
        try:
            img, new  = stream.read()
            if(last != new):
                last = new
                work_q.put_nowait(img)
                out_frames += 1
                starttime = starttime or time.time()
                print("img on queue")
            ret = result_q.get_nowait()
            proc_frames += 1
            # since Queue.get_nowait() throws an  exception on empty queue
            #   ret will always have a value
            printout(ret,time.time()-starttime,out_frames,proc_frames)
        except KeyboardInterrupt:   # terminate on ctrl-c
            break
        except queue.Empty:     # if  get_nowait() called on empty queue
            continue
    stream.stop()
    for process in processes:
        process.terminate()

def printout(ret,timedif,out_frames,proc_frames):
    # NOTE: HERE we do something with the returned position of the ant
    #       Currently, these are just output,
    print("{0}\tcX:{1}\tcY:{2}\tdirection:{3}".format(ret[3],ret[0], ret[1],ret[2]))
    print(timedif)
    print("Processing: {}".format(out_frames))
    print("Processed: {}".format(proc_frames))
