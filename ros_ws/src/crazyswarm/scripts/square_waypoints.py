#!/usr/bin/env python

from matplotlib.pyplot import waitforbuttonpress
import numpy as np
from pycrazyswarm import *

Z = 1.8

L = 1.0
waypoints = [
    (0,0,Z),
    (L, 0, Z),
    (L, L, Z),
    (0, L, Z),
    (0, 0, Z)
]

rgbs = [
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (0,1,0),
    (0,0,1)
]



if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    pos0s = [cf.position() for cf in allcfs.crazyflies]

    for cf in allcfs.crazyflies:
        cf.setParam("ring/effect", 7)

    for cf in allcfs.crazyflies:
        cf.takeoff(Z, 1.0+Z)
    
    timeHelper.sleep(1.5+Z)

    # go to each waypoint
    for j, p in enumerate(waypoints):
        for i, cf in enumerate(allcfs.crazyflies):
            cf.goTo(pos0s[i] + p, 0.0, 2.0)
            cf.setLEDColor(*rgbs[j])
        
        timeHelper.sleep(3.0)

    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)
