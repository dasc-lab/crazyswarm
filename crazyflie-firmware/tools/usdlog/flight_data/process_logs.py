import numpy as np
import rosbag
import pandas as pd
import matplotlib.pyplot as plt


for name in ['mine', 'no_barrier', 'no_safety', 'cbf']:

    bag = rosbag.Bag(name + '.bag')

    tf_ts = []
    tf_xs = []
    tf_ys = []
    tf_zs = []

    msg_start = None
    msg_end = None

    cmd_ts = []
    cmd_xs = []
    cmd_ys = []
    cmd_zs = []

    t_start = None

    for topic, msg, t in bag.read_messages(topics=['/tf']):

        if t_start is None:
            t_start = t.to_sec()

        tf_ts.append(t)
        tf_xs.append(msg.transforms[0].transform.translation.x)
        tf_ys.append(msg.transforms[0].transform.translation.y)
        tf_zs.append(msg.transforms[0].transform.translation.z)

    for topic, msg, t in bag.read_messages(topics=['/cf1/cmd_full_state']):
        if msg_start is None:
            msg_start = t

        cmd_ts.append(t)
        cmd_xs.append(msg.pose.position.x)
        cmd_ys.append(msg.pose.position.y)
        cmd_zs.append(msg.pose.position.z)

        
        msg_end = t

    bag.close()


    tf_ts_sec = [t.to_sec() - t_start for t in tf_ts]

    dict_tf = {
        'tf_ts': tf_ts_sec,
        'tf_xs': tf_xs,
        'tf_ys': tf_ys,
        'tf_zs': tf_zs,
    }

    df_tf = pd.DataFrame(dict_tf)

    df_tf.to_csv(name + '_tf_rosbag.csv')


    cmd_ts_sec = [t.to_sec()- t_start for t in cmd_ts]

    dict_cmd = {
        'cmd_ts': cmd_ts_sec,
        'cmd_xs': cmd_xs,
        'cmd_ys': cmd_ys,
        'cmd_zs': cmd_zs,
    }

    df_cmd = pd.DataFrame(dict_cmd)

    df_cmd.to_csv(name + '_cmd_rosbag.csv')

    print("done")