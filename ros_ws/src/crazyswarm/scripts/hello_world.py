"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

from pycrazyswarm import Crazyswarm




def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    t0 = timeHelper.time()
    state = "TAKEOFF"

    while not timeHelper.isShutdown():

        t = timeHelper.time() - t0
        p = cf.position()


        x = cf.getParam("stateEstimate/x")

        #print(f"{t:7.3f}: {state} {p[0]:7.3f} {p[1]:7.3f} {p[2]:7.3f}")
        print(x)


    return

    while not timeHelper.isShutdown():

        t = timeHelper.time() - t0
        p = cf.position()

        print(f"{t:7.3f}: {state} {p[0]:7.3f} {p[1]:7.3f} {p[2]:7.3f}")

        if state == "TAKEOFF":
            #cf.takeoff(targetHeight=1.0, duration=2.0)
            state = "POST_TAKEOFF"
            t_ref = t

        if state == "POST_TAKEOFF":
            if t >= t_ref + 2.0:
                state = "HOVER"
                t_ref = t

        if state == "HOVER":
            if t >= t_ref + 2.0:
                state = "LAND"

        if state == "LAND":
            #cf.land(targetHeight=0.04, duration=2.0)
            t_ref = t
            state = "POST_LAND"

        if state == "POST_LAND":
            if t - t_ref >= 2.0:
                break
        
        timeHelper.sleep(0.01)

if __name__ == "__main__":
    main()
