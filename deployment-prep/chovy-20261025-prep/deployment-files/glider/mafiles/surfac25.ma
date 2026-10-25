behavior_name=surface
# climb to surface with ballast pump full out
# pitch servo'ed to 26 degrees
# Hand Written
# 10 July 2010 ballsup@webbresearch.com based on legacy surfac10.ma
# 2017-08-24 lcooney@teledyne.com Added c_use_bpump 0 for Autoballast (M#1577)

# Come up when requested by science

<start:b_arg>

    b_arg: start_when(enum)         11 		  # BAW_SCI_SURFACE
    b_arg: end_action(enum)         1             # 0-quit, 1 wait for ^C quit/resume, 2 resume, 3 drift til "end_wpt_dist"
    b_arg: gps_wait_time(s)         300           # how long to wait for gps
    b_arg: keystroke_wait_time(sec) 300           # how long to wait for control-C
    b_arg: when_wpt_dist(m)         10            # how close to waypoint before surface, only if start_when==7
    b_arg: c_use_bpump(enum)    0  # use autoballast on surface climb (requires autoballast yo)
    b_arg: c_use_pitch(enum)        3             # 3:servo
    b_arg: c_pitch_value(X)         0.4538        # 26 deg

<end:b_arg>
