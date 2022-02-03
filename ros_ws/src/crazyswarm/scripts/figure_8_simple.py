#!/usr/bin/env python

from matplotlib.pyplot import waitforbuttonpress
import numpy as np
from pycrazyswarm import *

Z = 1.0
T = 7.0


OFFSETS = T/8;

def path(t):

    theta = 2*np.pi * t / T

    x = np.cos(theta + np.pi/2)
    y = 0.5*np.sin(2 * theta)
    z = Z

    return np.array([x,y,z])



if __name__ == "__main__":

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    pos0s = [np.array(cf.position()) for cf in allcfs.crazyflies]

    for cf in allcfs.crazyflies:
        cf.setParam("ring/effect", 7)
        cf.setLEDColor(0,0,1)

    for cf in allcfs.crazyflies:
        cf.takeoff(Z, 1.0+Z)
    
    timeHelper.sleep(1.5+Z)

    for i, cf in enumerate(allcfs.crazyflies):
        p0 = path(0 - i * OFFSETS)
        cf.goTo(p0, 0.0, 2.0)

    timeHelper.sleep(2.5)



    # start trajectory

    t0 = timeHelper.time()

    while timeHelper.time() - t0 <= 2*T:
        
        t = timeHelper.time() - t0

        for i, cf in enumerate(allcfs.crazyflies):
        
            cf.cmdPosition(path(t - i*OFFSETS), 0.0)

        timeHelper.sleepForRate(50)

    for cf in allcfs.crazyflies:
        cf.land(targetHeight=0.02, duration=4.0)
    
    timeHelper.sleep(5.0)
