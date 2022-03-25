#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *


Z = 1.0
sleepRate = 30


def goCircle(timeHelper, cf, period, radius, kPosition, maxTime):
        startTime = timeHelper.time()
        pos = cf.position()
        startPos = cf.initialPosition + np.array([0, 0, Z])
        center_circle = startPos - np.array([radius, 0, 0])
        while timeHelper.time() - startTime <= maxTime:
            if timeHelper.time() - startTime <= maxTime - 0.1:
                cf.notifySetpointsStop()
            time = timeHelper.time() - startTime
            omega = 2 * np.pi / period
            vx = -radius * omega * np.sin(omega * time)  
            vy = radius * omega * np.cos(omega * time)
            desiredPos = center_circle + radius * np.array(
                [np.cos(omega * time), np.sin(omega * time), 0])
            errorX = desiredPos - cf.position() 
            cf.cmdVelocityWorld(np.array([vx, vy, 0] + kPosition * errorX), yawRate=0)
            timeHelper.sleepForRate(sleepRate)

        while timeHelper.time() - startTime <= maxTime + 0.5:
            cf.cmdVelocityWorld(np.zeros(3), yawRate=0.0)
            timeHelper.sleepForRate(sleepRate)
            
        cf.goTo(startPos, 0, 2.0)
        timeHelper.sleep(2.0+1.0)
        


if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(2 + Z)
    goCircle(timeHelper, allcfs.crazyflies[0], period=4, radius=1, kPosition=1, maxTime=4.0)

    allcfs.land(targetHeight=0.03, duration=1.0+Z)
    timeHelper.sleep(2+Z)

