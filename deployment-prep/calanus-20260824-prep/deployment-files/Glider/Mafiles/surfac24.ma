behavior_name=surface

# climb to surface with autoballast values
# pitch servo'ed to 26 degrees

# Come up every way point

<start:b_arg>

    b_arg: start_when(enum)         8             # BAW_WHEN_HIT_WAYPOINT = 8, when hit a waypoint

    b_arg: end_action(enum)         1             # 0-quit, 1 wait for ^C quit/resume, 2 resume, 3 drift til "end_wpt_dist"
    b_arg: gps_wait_time(s)         300           # how long to wait for gps
    b_arg: keystroke_wait_time(sec) 599           # how long to wait for control-C
    b_arg: printout_cycle_time(sec) 30.0          # How often to print dialog

 # Climb arguments when this surface behavior becomes active 
   ## Pump arguments
    b_arg: c_use_bpump(enum)        0             # use autoballast on surface climb (requires autoballast yo)

   ## Pitch arguments
    b_arg: c_use_pitch(enum)        3             # 3:servo
    b_arg: c_pitch_value(X)         0.4538        # 26 deg

<end:b_arg>

