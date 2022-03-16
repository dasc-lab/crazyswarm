#!/usr/bin/env python

from turtle import pos
import numpy as np

from pycrazyswarm import *
import uav_trajectory


def acceleration_command(pos_err, vel_err):
    kp = 2.24
    kd = 4.23

    # kp = 2.0
    # kd = 1.0
    corr = -kp*pos_err -kd*vel_err
    print(corr)
    return corr
    

def executeTrajectory(timeHelper, cf, trajpath, rate=100, offset=np.zeros(3)):
    traj = uav_trajectory.Trajectory()
    traj.loadcsv(trajpath)

    STAB_TIME  = 4.0
    

    print("DURATION: ", traj.duration)
    curr_pos = cf.position()
    start_time = timeHelper.time()
    while not timeHelper.isShutdown():
        t = timeHelper.time() - start_time
        # print(t, traj.duration)

        if t >= traj.duration + 2*STAB_TIME -0.2:
            print("NOTIFYING STOP")
            cf.notifySetpointsStop()

        if t >= traj.duration + 2*STAB_TIME:
            print("FINISHED TRAJ")
            return
            # e = traj.eval(traj.duration)
            # return e.pos + np.array(cf.initialPosition) + offset, e.yaw

        # FACTOR = 10
        t = min(traj.duration, max(t-STAB_TIME, 0))
        e = traj.eval(t)

        des_pos = e.pos + np.array(cf.initialPosition) + offset
        # des_pos = des_pos
        des_vel = e.vel
        des_acc = e.acc
        des_yaw = e.yaw
        des_omg = e.omega

        # if des_pos[0] >= 0.5:
        #     des_pos[0] = 0.5
        #     des_vel[0] = 0.0
        #     des_acc[0] = 0.0


        tmp_pos = cf.position()
        curr_vel = (tmp_pos - curr_pos) * rate
        curr_pos = cf.position()

        cmd_acc = des_acc + acceleration_command(curr_pos - des_pos, curr_vel - des_vel)
        
        ############# SEND

        des_pos[0] = -100.0 # make it acceleration mode!
        cf.cmdFullState(
            des_pos,
            des_vel,
            cmd_acc,
            des_yaw,
            des_omg)

        timeHelper.sleepForRate(rate)


if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    rate = 50.0
    Z = 1.0

    print("TAKEOFF")
    cf.takeoff(targetHeight=Z, duration=Z+1.0)
    timeHelper.sleep(Z+1.25)

    print("EXECUTING")
    # last_pos, last_yaw = executeTrajectory(timeHelper, cf, "figure8.csv", rate, offset=np.array([0, 0,Z]))
    # cf.goTo(last_pos, last_yaw, 1.0)
    # timeHelper.sleep(3.0)

    


    executeTrajectory(timeHelper, cf, "figure8.csv", rate, offset=np.array([0, 0,Z]))

    cf.goTo(cf.position(), 0.0, 1.0)
    # # cf.goTo(last_pos, last_yaw, 1.0)
    print("LANDING")
    timeHelper.sleep(0.8)


    cf.land(targetHeight=0.03, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)
