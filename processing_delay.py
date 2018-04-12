import time
import timeit
import cv2
import json
from matplotlib import pyplot as plt
import antdetector

# setup
img = cv2.imread('images/Carpenter-Ant.jpg')
options = json.load(open("test_options.json"))
img = cv2.resize(img,(options["resX"],options["resY"]), interpolation = cv2.INTER_CUBIC)
ad = antdetector.AntDetector(options)
#
for i in timeit.repeat('ad.process(img)',number=options["number"],repeat=options["repititions"],globals=globals()) :
    print(i)
