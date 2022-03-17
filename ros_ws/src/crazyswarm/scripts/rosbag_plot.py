from matplotlib import lines
import rosbag
import numpy as np

import glob
import os

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

T_STAB = 0.0
X_BARR = 0.5

files = glob.glob("../bags/*.bag")

latest_file = max(files, key=os.path.getctime)

bag = rosbag.Bag(latest_file, 'r')

ts = []
xs = []
ys = []
zs = []


cmd_ts = []
cmd_xs = []
cmd_ys = []
cmd_zs = []

start = False

start_t = None
last_t = None

for topic, msg, t in bag.read_messages(topics='/cf1/cmd_full_state'):

    if start is False:
        print(msg)
        start=True
        start_t = t.to_sec()
    
    cmd_ts.append(t.to_sec())
    cmd_xs.append(msg.pose.position.x)
    cmd_ys.append(msg.pose.position.y)
    cmd_zs.append(msg.pose.position.z)
    last_t = t.to_sec()


for topic, msg, t in bag.read_messages(topics=['/tf']):

    

    trans = msg.transforms[0].transform.translation

    ts.append(t.to_sec())
    xs.append(trans.x)
    ys.append(trans.y)
    zs.append(trans.z)




bag.close()

start_t = start_t + T_STAB

# print(start_t, last_t)

cmd_inds = [i for i in range(len(ts)) if (ts[i] >= start_t) and (ts[i] <= last_t)]

ts = [t - ts[0] for t in ts]

ts = np.array(ts)
xs = np.array(xs)
ys = np.array(ys)
zs = np.array(zs)


cmd_ts = np.array(cmd_ts)
cmd_xs = np.array(cmd_xs)
cmd_ys = np.array(cmd_ys)
cmd_zs = np.array(cmd_zs)

fig = plt.figure()
ax = plt.axes(projection = '3d')

ax.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))

ax.plot3D(xs, ys, zs)


ax.plot3D(xs[cmd_inds], ys[cmd_inds], zs[cmd_inds], color="red")

ax.plot3D(cmd_xs, cmd_ys, cmd_zs, ".g")

fig = plt.figure()
plt.plot(xs[cmd_inds], ys[cmd_inds], color="red")
plt.plot(cmd_xs, cmd_ys, 'g.')

plt.gca().set_aspect('equal')
plt.axvline(x=X_BARR, linestyle='--')
plt.show()