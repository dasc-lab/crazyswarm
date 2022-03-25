#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

Z = 1.0

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    pos0s = [cf.position() for cf in allcfs.crazyflies]
    
    allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)
    for i, cf in enumerate(allcfs.crazyflies):
        pos = np.array(pos0s[i]) + np.array([0, 0, Z])
        cf.goTo(pos, 0, 1.0)
        # go to this position with yaw 0 in 1 second. then hold it there
        

    #print("press button to continue...")
    #swarm.input.waitUntilButtonPressed()

    timeHelper.sleep(2.0)

    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)
