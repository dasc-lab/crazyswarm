import pickle
import numpy as np
import matplotlib.pyplot as plt

from scipy import signal


def norm(s):
    return np.sqrt(s*s)

file = open('logs.pkl', 'rb')

data = pickle.load(file)

file.close()

# plt.figure()
# plt.plot(data["t"], [x[0] for x in data["est_pos"]], label="est_x")
# plt.plot(data["t"], [x[0] for x in data["meas_pos"]], label="meas_x")

# plt.figure()
# plt.plot(data["t"], [x[1] for x in data["est_pos"]], label="est_y")
# plt.plot(data["t"], [x[1] for x in data["meas_pos"]], label="meas_y")

# plt.figure()
# plt.plot(data["t"], [x[2] for x in data["est_pos"]], label="est_z")
# plt.plot(data["t"], [x[2] for x in data["meas_pos"]], label="meas_z")


# plt.figure()
# plt.plot(data["t"], [x[0] for x in data["est_vel"]], label="est_vx")

# plt.show()


plt.figure()
plt.plot(data["t"], [x[0] for x in data["est_pos"]], label="est_x")
plt.plot(data["t"], [x[0] for x in data["meas_pos"]], label="meas_x")

# plt.figure()
# plt.plot(data["t"], [x[1] for x in data["est_pos"]], label="est_y")
# plt.plot(data["t"], [x[1] for x in data["meas_pos"]], label="meas_y")

# plt.figure()
# plt.plot(data["t"], [x[2] for x in data["est_pos"]], label="est_z")
# plt.plot(data["t"], [x[2] for x in data["meas_pos"]], label="meas_z")



# vel

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

plt.figure()
plt.plot(data["t"], est_v_x, label="est_vx")
plt.plot(data["t"], filt_vel_x, label="savgol")
plt.legend()

# plt.figure()
# plt.plot(data["t"], est_v_y, label="est_vy")
# plt.plot(data["t"], filt_vel_y, label="savgol")
# plt.legend()

# plt.figure()
# plt.plot(data["t"], est_v_z, label="est_vz")
# plt.plot(data["t"], filt_vel_z, label="savgol")
# plt.legend()


plt.figure()

plt.plot(data["t"], [norm(s) for s in (est_x - meas_x)])
plt.plot(data["t"], [norm(s) for s in (est_v_x - filt_vel_x)])


# commands

plt.figure()
plt.plot(data["t"], [x[0] for x in data["cmd_acc"]])
plt.plot(data["t"], [x[0] for x in data["safe_acc"]])



plt.show()


