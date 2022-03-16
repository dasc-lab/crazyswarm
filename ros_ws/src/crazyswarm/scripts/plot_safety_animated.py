import pickle
import numpy as np
import matplotlib.pyplot as plt

from scipy import signal


def norm(s):
    return np.sqrt(s*s)

names = ['nominal', 'baseline', 'approach_1', 'approach_2']

for name in names:
    # file = open('logs.pkl', 'rb')
    file = open('logs_'+name+'.pkl', 'rb')

    data = pickle.load(file)

    file.close()


    # extract data

    ts = data["t"]

    est_x = np.array([x[0] for x in data["est_pos"]])
    est_y = np.array([x[1] for x in data["est_pos"]])
    est_z = np.array([x[2] for x in data["est_pos"]])


    meas_x = np.array([x[0] for x in data["meas_pos"]])
    meas_y = np.array([x[1] for x in data["meas_pos"]])
    meas_z = np.array([x[2] for x in data["meas_pos"]])

    est_v_x = np.array([x[0] for x in data["est_vel"]])
    est_v_y = np.array([x[1] for x in data["est_vel"]])
    est_v_z = np.array([x[2] for x in data["est_vel"]])

    window = 25
    order = 3

    filt_vel_x = signal.savgol_filter(meas_x, window, order, deriv=1, delta=(1.0/50))
    filt_vel_y = signal.savgol_filter(meas_y, window, order, deriv=1, delta=(1.0/50))
    filt_vel_z = signal.savgol_filter(meas_z, window, order, deriv=1, delta=(1.0/50))

    fig = plt.figure()
    ax = plt.axes(projection = '3d')


    # ax.set_box_aspect((np.ptp(est_x), np.ptp(est_y), np.ptp(est_z)))

    # ax.plot3D(est_x, est_y, est_z, label="est")

    safe_inds = [i for i in range(len(meas_x)) if meas_x[i] <= 0.75 and i >= 4*50]
    unsafe_inds = [i for i in range(len(meas_x)) if meas_x[i] > 0.75 and i >= 4*50]



    surf_x = np.array([[0.75, 0.75], [0.75, 0.75]])
    surf_y = np.array([[1.5, -1.5], [1.5, -1.5]])
    surf_z = np.array([[0, 0], [1.5, 1.5]])
    ax.axes.set_zlim3d(bottom=0.0, top=1.5)
    ax.view_init(elev=45, azim=120)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m]")


    ax.plot3D(meas_x[unsafe_inds], meas_y[unsafe_inds], meas_z[unsafe_inds], '.r')
    ax.plot_surface(surf_x, surf_y, surf_z, alpha=0.45)
    ax.plot3D(meas_x[safe_inds], meas_y[safe_inds], meas_z[safe_inds], '.g')

    plt.savefig("path_"+ name + ".png")
