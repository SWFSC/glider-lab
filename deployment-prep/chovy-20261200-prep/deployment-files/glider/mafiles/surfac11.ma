behavior_name=surface
# climb to surface with ballast pump full out and thruster depth rate control
# pitch servo'ed to 26 degrees
# Hand Written
# 2014-Oct-02 lacooney@alum.mit.edu Initial, copied from surfac01.ma

# Come up if haven't had comms for a while, 20 minutes. 

<start:b_arg>

    b_arg: start_when(enum)         12            # BAW_NOCOMM_SECS 12, when have not had comms for WHEN_SECS secs

    b_arg: when_secs(sec)           1200          # Surface every 20 min for no comms

    b_arg: end_action(enum)         1             # 0-quit, 1 wait for ^C quit/resume, 2 resume, 3 drift til "end_wpt_dist"
    b_arg: gps_wait_time(s)         300           # how long to wait for gps
    b_arg: keystroke_wait_time(sec) 300           # how long to wait for control-C
    b_arg: when_wpt_dist(m)         10            # how close to waypoint before surface, only if start_when==7
    b_arg: c_use_pitch(enum)        3             # 3:servo
    b_arg: c_pitch_value(X)         0.4538        # 26 deg
    b_arg: printout_cycle_time(sec) 60.0 # How often to print dialog
    b_arg: c_use_thruster(enum)   3               # 3  Command depth rate.  See sensors for use_thruster = depthrate	
    b_arg: c_thruster_value(X)   -0.04            # use_thruster == 3  m/s, desired depth rate. < 0 for climb
    b_arg: c_stop_when_air_pump(bool)  1        # Terminate climb once air pump has been inflated. For use with thruster only.
<end:b_arg>

 
