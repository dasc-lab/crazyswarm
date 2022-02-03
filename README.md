![Crazyswarm ROS CI](https://github.com/USC-ACTLab/crazyswarm/workflows/Crazyswarm%20ROS%20CI/badge.svg)
![Sim-Only Conda CI](https://github.com/USC-ACTLab/crazyswarm/workflows/Sim-Only%20Conda%20CI/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/crazyswarm/badge/?version=latest)](https://crazyswarm.readthedocs.io/en/latest/?badge=latest)

# Crazyswarm
A Large Nano-Quadcopter Swarm.

The documentation is available here: http://crazyswarm.readthedocs.io/en/latest/.

## Troubleshooting
Please start a [Discussion](https://github.com/USC-ACTLab/crazyswarm/discussions) for...

- Getting Crazyswarm to work with your hardware setup.
- Advice on how to use the [Crazyswarm Python API](https://crazyswarm.readthedocs.io/en/latest/api.html) to achieve your goals.
- Rough ideas for a new feature.

Please open an [Issue](https://github.com/USC-ACTLab/crazyswarm/issues) if you believe that fixing your problem will involve a **change in the Crazyswarm source code**, rather than your own configuration files. For example...

- Bug reports.
- New feature proposals with details.




# QUICK START

Quick start guide on setting up crazyflies for our lab. 

The official documentation in crazyswarm is pretty good. Id highly recommend reading that too/first. 


## Software Installation

As of Feb 2 2022, Ubuntu 20 installation worked, but ubuntu 18 did not work for us. Some issue in the libmotioncapture sdk. 

You will need
1. ROS
2. cfclient (`python3 -m pip install cfclient`)
3. cflib (Optional, will be autoinstalled by cfclient) (`python3 -m pip install cflib`) 
4. crazyswarm (Follow instructions at https://crazyswarm.readthedocs.io/en/latest/installation.html)
5. We used Ubuntu 20, and Python3


## Hardware Setup


1. Update the radio firmware following instructions here: https://github.com/bitcraze/crazyradio-firmware
Note, you should always use `python3` commands, not `python` as some of the documentation suggests.
The radio module is labelled with "PA" on radios in our lab.
2. If you get 'No module named `usb` run `python3 -m pip install pyusb`
3. Update the firmware on the quad using instructions here: https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/building-and-flashing/build/ or using the cfclient
4. Connect crazyradio to the usb port. 
5. Connect battery to crazyflie. Note the number of the crazyflie, as this is the ID of the drone. 
6. Open cfclient (In terminal `cfclient`)
7. Where you see Addreses (near top left) set the address in the following form `0xE7E7E7E7<ID>` where `<ID>` is the quad's id.
8. Hit Scan
9. You should see the interface switch to something like `radio://0/40/2M/E7E7E7E7<ID>` where the first arg is the usb device number (assigned by Ubuntu) the second is the channel number (needed later) the third is the data rate (eg 2M), and the fourth is the uri of the quad.
10. It should now have connected to the quad. Moving the quad should move the horizon. 
11. Create a object in vicon tracker for this quad. Call the object `cf<ID>`, for instance, for crazyflie id 7, it should be labelled `cf7`. Make sure the forward direction on the quad is aligned to the +X axis of the vicon room.

## First Flight

IN TERMINAL 1: 

1. `cd crazyswarm` the package provided by crazyswarm
2. `export CSW_PYTHON=python3`
3. `./build.sh` to build the project (build is used instead of catkin_make or anything similar)
4. `cd ros_ws` and `source devel/setup.bash`
5.  Next, we run through configuration: https://crazyswarm.readthedocs.io/en/latest/configuration.html#
6. Configure  `crazyswarm/ros_ws/src/crazyswarm/launch/allcrazyflies.yaml` Here, add a config for each crazyflie you will be running. Use the ID, channel etc from earlier setup. The initial position will be ignored if using motionCapture. Type='default' for the small crazyflies. 
7. Choose which crazyflies will be run in current experiment. `cd crazyswarm/ros_ws/src/crazyswarm/scripts` and run `python3 chooser.py` Use the checkboxes to select which quads are running. This will immediately replace `crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml`, which is what is used in the final launch script. 
8. Edit the launch script in `crazyswarm/ros_ws/src/crazyswarm/launch/hover_swarm.launch` Mainly, you need to specify `motion_capture_type: "vicon", `motion_capture_host_name: <IP ADDRESS OF MOCAP COMPUTER>` and `object_tracking_type: "motionCapture"` I also commented out the teleop and joy nodes that were in the script originally, but that is upto you. 
9. Ensure vicon is running
10. Launch the launch script: `roslaunch crazyswarm hover_swarm.launch`
  You should see a rviz window pop up, and the the quad should be visible in it. 
  
IN TERMINAL 2: 
1. `cd crazyswawm/ros_ws`
2. `source devel/setup.bash`
3. `cd src/crazyswarm/scripts`
4. `python3 niceHover.py`
  
  This should launch the drone, and make it hover!
  
  
  
  
  ## Two Quad Figure of 8
  
  1. update `allcrazyflies.yaml` appropriately and run `python3 chooser.py` to set the correct quads up. 
  2. source the `ros_ws/devel/setup.py` in each terminal.
  3. In one terminal run `roslaunch crazyswarm hover_launch.launch`
  4. In a second terminal run `python3 figure_8_simple.py`
  
