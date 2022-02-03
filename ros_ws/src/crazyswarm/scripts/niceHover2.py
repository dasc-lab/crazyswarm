#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

Z = 1.0

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    cf = allcfs.crazyflies[0]

    pos0 = cf.position()

    cf.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(1.5+Z)
    # # pos = np.array(pos0) + np.array([0, 0, Z])
    # pos = np.copy(cf.position())
    cf.goTo([0,0,1.0], 0, 1.0)
    # cf.goTo(pos, 0.0, 1.0)

    # while not timeHelper.isShutdown():
    #     cf.cmdPosition(pos, yaw=0.0)
    #     timeHelper.sleepForRate(50)    

    timeHelper.sleep(5.0)

    # #print("press button to continue...")
    # #swarm.input.waitUntilButtonPressed()

    # timeHelper.sleep(2.0)

    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)
