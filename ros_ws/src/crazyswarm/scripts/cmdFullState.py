#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import uav_trajectory


def executeTrajectory(timeHelper, cf, trajpath, rate=100, offset=np.zeros(3)):
    traj = uav_trajectory.Trajectory()
    traj.loadcsv(trajpath)

    print("DURATION: ", traj.duration)

    start_time = timeHelper.time()
    while not timeHelper.isShutdown():
        t = timeHelper.time() - start_time
        print(t, traj.duration)
        if t >= traj.duration-0.1:
            print("FINISHED TRAJ")
            e = traj.eval(traj.duration)
            return e.pos + np.array(cf.initialPosition) + offset, e.yaw

        e = traj.eval(t)
        cf.cmdFullState(
            e.pos + np.array(cf.initialPosition) + offset,
            e.vel,
            e.acc,
            e.yaw,
            e.omega)

        timeHelper.sleepForRate(rate)


if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    rate = 50.0
    Z = 0.5

    print("TAKEOFF")
    cf.takeoff(targetHeight=Z, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)

    print("EXECUTING")
    last_pos, last_yaw = executeTrajectory(timeHelper, cf, "figure8.csv", rate, offset=np.array([0, 0, 0.5]))
    # timeHelper.sleep(3.0)

    print("LANDING")
    cf.notifySetpointsStop()

    cf.goTo(last_pos, last_yaw, 1.0)

    timeHelper.sleep(3.0)


    cf.land(targetHeight=0.03, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)
