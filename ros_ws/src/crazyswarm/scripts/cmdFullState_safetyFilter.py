#!/usr/bin/env python

import posix
from re import M
from turtle import pos, update
import numpy as np

from pycrazyswarm import *
import uav_trajectory

import pickle

save_t = []
save_meas_pos = []
save_est_pos = []
save_est_vel = []
save_cmd_acc = []
save_safe_acc = []


def predict_state(pos, vel, acc, dt):
    return pos + vel * dt + acc * 0.5 * dt**2, vel + acc*dt

def correct_state(pos, vel, measured_pos):
    L1 = 0.3016
    L2 = 2.02
    return pos + L1 * (measured_pos - pos), vel + L2 * (measured_pos - pos)


def  safety_filter_baseline(cmd_acc, curr_pos, curr_vel):

    # return 1.0*cmd_acc

    x = curr_pos[0]
    vx = curr_vel[0]
    ux_des = cmd_acc[0]

    x_bar = 0.75
    alpha0 = 2.0
    alpha1 = 2.0

    h_nom = x_bar - x
    Lfh_nom = - vx

    h = Lfh_nom + alpha0 * h_nom

    Lfh = alpha0 * vx
    Lgh = -1

    # constraint is Lfh + Lgh u >= -alpha1 h
    
    if Lfh + Lgh * ux_des + alpha1 * h >= 0.0:
        return 1.0*cmd_acc

    ux_safe = -(Lfh + alpha1*h)/Lgh

    u_safe = np.array([ux_safe, cmd_acc[1], cmd_acc[2]])

    print("CORRECTING! ", ux_safe - ux_des)

    
    return u_safe


def  safety_filter_approach_1(cmd_acc, curr_pos, curr_vel, meas_pos, t):

    # return 1.0*cmd_acc

    x = curr_pos[0]
    vx = curr_vel[0]
    ux_des = cmd_acc[0]

    x_bar = 0.75
    alpha0 = 2.0
    alpha1 = 2.0

    h_nom = x_bar - x
    Lfh_nom = - vx

    h = Lfh_nom + alpha0 * h_nom

    Lfh = alpha0 * vx
    Lgh = -1

    # observer gains in continuous time
    L1 = 15.1774
    L2 = 115.1774

    Llh = alpha0 * L1 - L2

    M = 0.35
    Mdot = 0.0
    gammah = np.sqrt(1.0 + alpha0**2)

    # constraint is Lfh + Lgh u + Llh*(y-Cx) >= -alpha1 (h - gammah*M) + gammah * Mdot

    left_hand_side = Lfh + Llh * (meas_pos[0] - curr_pos[0]) + alpha1 * (h - gammah * M) - gammah * Mdot

    if left_hand_side + Lgh * ux_des >= 0.0:
        return 1.0*cmd_acc

    ux_safe = -(left_hand_side)/Lgh

    u_safe = np.array([ux_safe, cmd_acc[1], cmd_acc[2]])

    print("CORRECTING! ", ux_safe - ux_des)
    
    return u_safe


def  safety_filter_approach_2(cmd_acc, curr_pos, curr_vel):


    x = curr_pos[0]
    vx = curr_vel[0]
    ux_des = cmd_acc[0]

    x_bar = 0.75
    alpha0 = 2.0
    alpha1 = 2.0

    h_nom = x_bar - x
    Lfh_nom = - vx

    h = Lfh_nom + alpha0 * h_nom

    Lfh = alpha0 * vx
    Lgh = -1

    M = 0.35
    Mdot = 0.0
    gammah = np.sqrt(1.0 + alpha0**2)
    gammaLfhalphah = np.sqrt(((alpha0-alpha1)**2 + (alpha0 * alpha1)**2))

    # constraint is Lfh + Lgh u + Llh*(y-Cx) >= -alpha1 (h - gammah*M) + gammah * Mdot

    left_hand_side = Lfh + alpha1*h - gammaLfhalphah* M

    if left_hand_side + Lgh * ux_des >= 0.0:
        return 1.0*cmd_acc

    ux_safe = -(left_hand_side)/Lgh

    u_safe = np.array([ux_safe, cmd_acc[1], cmd_acc[2]])

    print("CORRECTING! ", ux_safe - ux_des)
    
    return u_safe


def acceleration_command(pos_err, vel_err, des_acc):
    # kp = 8.87
    # kd = 10.85
    kp = 12.0397
    kd = 14.0203

    corr = -kp*pos_err -kd*vel_err
    corr[2] = 0.0 # dont correct z acceleration, since the firmware handles z separately

    # corr = corr
    # print(corr)
    return des_acc + corr
    

def executeTrajectory(timeHelper, cf, trajpath, rate=100, offset=np.zeros(3)):
    traj = uav_trajectory.Trajectory()
    traj.loadcsv(trajpath)

    FACTOR=1

    STAB_TIME  = 4.0
    
    est_pos = cf.position()
    est_vel = np.zeros(3)

    print("DURATION: ", FACTOR*traj.duration)
    curr_pos = cf.position()
    start_time = timeHelper.time()

    while not timeHelper.isShutdown():
        t = timeHelper.time() - start_time
        # print(t, traj.duration)

        if t >= FACTOR*traj.duration + 2*STAB_TIME -0.2:
            # print("NOTIFYING STOP")
            cf.notifySetpointsStop()

        if t >= FACTOR*traj.duration + 2*STAB_TIME:
            print("FINISHED TRAJ")
            return

        # Measurement CORRECTION
        meas_pos = cf.position()

        ## compute commmand accel
        t_traj = min(FACTOR*traj.duration, max(t-STAB_TIME, 0))        

        e = traj.eval(t_traj/FACTOR)

        des_pos = e.pos + np.array(cf.initialPosition) + offset
        des_vel = e.vel/FACTOR
        des_acc = e.acc/(FACTOR**2)
        des_yaw = e.yaw
        des_omg = e.omega/(FACTOR)

        cmd_acc = acceleration_command(est_pos - des_pos, est_vel - des_vel, des_acc)


        ## compute safety filter
        # safe_acc = 1.0*cmd_acc
        # safe_acc = safety_filter_baseline(cmd_acc, est_pos, est_vel)
        # safe_acc = safety_filter_approach_1(cmd_acc, est_pos, est_vel, meas_pos, t)
        safe_acc = safety_filter_approach_2(cmd_acc, est_pos, est_vel)

        ## state estimation
        est_pos, est_vel = correct_state(est_pos, est_vel, meas_pos)
        est_pos, est_vel = predict_state(est_pos, est_vel, safe_acc, 1.0/rate)

        
        ### SAVE
        save_t.append(t)
        save_est_pos.append(est_pos)
        save_est_vel.append(est_vel)
        save_meas_pos.append(meas_pos)
        save_cmd_acc.append(cmd_acc)
        save_safe_acc.append(safe_acc)

        ############# SEND

        # des_pos[0] = -100.0 # make it acceleration mode!
        cf.cmdFullState(
            des_pos,
            des_vel,
            safe_acc,
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
    timeHelper.sleep(Z+0.9)

    print("EXECUTING")
    executeTrajectory(timeHelper, cf, "figure8.csv", rate, offset=np.array([0, 0,Z]))

    # cf.goTo(cf.position(), 0.0, 1.0)
    print("LANDING")
    # timeHelper.sleep(0.8)


    cf.land(targetHeight=0.03, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)

    file = open('logs.pkl', 'wb')

    saves = {
        "t" : save_t , 
        "meas_pos" : save_meas_pos , 
        "est_pos": save_est_pos, 
        "est_vel" : save_est_vel , 
        "cmd_acc" : save_cmd_acc , 
        "safe_acc" : save_safe_acc
    }

    pickle.dump(saves, file)

    file.close()
