# -*- coding: utf-8 -*-
"""
example on how to plot decoded sensor data from crazyflie
@author: jsschell
"""
import CF_functions as cff
import matplotlib.pyplot as plt
import re
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

# decode binary log data
logData = cff.decode(args.filename)

print()
print()
print()

print("*** THE KEYS ARE: ")

keys = logData.keys()
print(keys)

N = len(logData['tick'])

for k in keys:
    print(k)
    assert(N == len(logData[k]))

df = pd.DataFrame({k:list(v) for k,v in logData.items()})

print(df)

df.to_csv(args.filename + ".csv")

print("SAVED!")

ts = logData["tick"]
xs = logData["ctrlGeo.log_state_x"]
ys = logData["ctrlGeo.log_state_y"]
zs = logData["ctrlGeo.log_state_z"]

std_x = [4 * np.sqrt(x) for x in logData["ctrlGeo.log_state_cov_vx"]]


plt.figure()
plt.title("Cov x")
plt.plot(logData["tick"], std_x)



plt.figure()
plt.title(" x- y - z")
ax = plt.axes(projection = '3d')

safe_inds = [i for i in range(len(xs)) if xs[i] <= 0.5]
unsafe_inds = [i for i in range(len(xs)) if xs[i] > 0.5]



surf_x = np.array([[0.5, 0.5], [0.5, 0.5]])
surf_y = np.array([[1.5, -1.5], [1.5, -1.5]])
surf_z = np.array([[0, 0], [1.5, 1.5]])
ax.axes.set_zlim3d(bottom=0.0, top=1.5)
ax.view_init(elev=45, azim=120)

ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_zlabel("z [m]")


ax.plot3D(xs[unsafe_inds], ys[unsafe_inds], zs[unsafe_inds], '.r')
ax.plot_surface(surf_x, surf_y, surf_z, alpha=0.45)
ax.plot3D(xs[safe_inds], ys[safe_inds], zs[safe_inds], '.g')
plt.show()