behavior_name=drift_at_depth
# drift_12.ma
# Contains all drift_at_depth behavior arguments
# This behavior performs a thruster-assisted 'bathtub' profile.
# The glider dives to the target depth or altitude, drifts there and 
# turns on the thruster for the specified amount of time, and then surfaces. 
# After surfacing, the drift behavior resumes after a ctrl-C quit/resume.
#
# Important note: If the thruster is not being used, do not use this file.  It assumes that the thruster
# will be installed to provide depth control and will rely less on the buoyancy engine
#
# Primary sensors for the user to modify:
# b_arg: stop_when_hover_for(sec) 600.0 # terminate hover when depth does not change for
# b_arg: target_depth(m)        15.0 # depth to drift at
# b_arg: target_altitude(m)     10.0 # altitude to drift at, <=0 disables
# b_arg: thruster_value(X)   6  # use_thruster == 4  watt, desired input power
#
# 2013-Apr-24 lacooney@alum.mit.edu Initial
# 2014-Oct-02 lacooney@alum.mit.edu Added comment for use_thruster range
# 2015-08-21 lacooney@alum.mit.edu Added items to uncomment for deep pump, M#2327
# 2016-03-28 lcooney@teledyne.com Added battpos_db=0.2 M#2626
# 2017-08-09 lcooney@teledyne.com Changed d/c_climb_bpump to -/+260 M#3389 

<start:b_arg>
    b_arg: start_when(enum) 2      # See doco below, allowable=0,1,2,3,4,6,7,8,9,10,13

    b_arg: end_action(enum) 2     # 0-quit, 2-resume
    b_arg: stop_when_hover_for(sec) 600.0 # terminate hover when depth does not change for
                                           # this many secs, <0 to disable
										   # Not recommended longer than 7200
    b_arg: est_time_to_settle(s) 30.0  # Used to force invalid cc_time_til_inflect for this
                                        # many seconds at the beginning of the behavior.

    b_arg: target_depth(m)        15.0 # depth to drift at

    b_arg: target_altitude(m)     15.0 # altitude to drift at, <=0 disables
    b_arg: alt_time(s)           0.0 # time spacing for altimeter pings
                                       # <0 is off, =0 as fast as possible
                                       # >0 that many seconds betweens measurements
### Shallow pump values
#    b_arg: target_deadband(m)      0.1 # +/- around target depth
#    b_arg: start_dist_from_target(m) 1.0 # start the drift this distance from the target depth/altitude.  -1 means use the target_deadband
#    b_arg: depth_ctrl(enum)          2 # 2: pitch-based depth control: see 'pitching depth control mode' sensors
#    b_arg: bpump_delta_value(cc)   2.0 # Increments to adjust x_hover_ballast(cc) to obtain
#                                       # neutral buoyancy (>= 1.0 cc).
#
#    b_arg: bpump_deadz_width(cc)  30.0 # For temporarily adjusting the buoyancy pump
#    b_arg: bpump_db_frac_dz(nodim) 0.1 # deadband during the drift_at_depth behavior
#    b_arg: bpump_delay(s)          0.0 

### Deep pump values
    b_arg: target_deadband(m)      5 # +/- around target depth
    b_arg: start_dist_from_target(m) 7.0 # start the drift this distance from the target depth/altitude.  -1 means use the target_deadband
    b_arg: depth_ctrl(enum)          2 # 2: pitch-based depth control: see 'pitching depth control mode' sensors
    b_arg: bpump_delta_value(cc)   10.0 # Increments to adjust x_hover_ballast(cc) to obtain
                                       # neutral buoyancy (>= 1.0 cc).

    b_arg: bpump_deadz_width(cc)  30.0 # For temporarily adjusting the buoyancy pump
    b_arg: bpump_db_frac_dz(nodim) 0.667 # deadband during the drift_at_depth behavior
    b_arg: bpump_delay(s)          90 

    	# Arguments for hovering
                                   # pitch_mode_t values - battery or fluid fore/aft control
    b_arg: use_pitch(enum) 3       # 4  Fluid Pumped absolute
                                   # 3  Servo on Pitch
                                   # 2  Pitch, set once from curve
                                   # 1  BattPos
    b_arg: pitch_value(X) 0.0  # use_pitch == 4    cc, clips to max legal, >0 to nose down
                                   # use_pitch == 2,3  rad, desired pitch angle, <0 to dive
                                   # use_pitch == 1    in,  desired battpos, >0 to nose down
                                   #                     clips to max legal
    b_arg: wait_for_pitch(bool) 1


    b_arg: use_thruster(enum)   4  # 0  Not in use
                                   # 1  Command input voltage (as % of glider voltage)
                                   # 2  Command input voltage (as % of max thruster input voltage)	
                                   # 3  N/A for this behavior
                                   # 4  Command input power. See sensors for use_thruster = power										
    b_arg: thruster_value(X)   6.0  # use_thruster == 0  None
                                   # use_thruster == 1  %, desired % of glider voltage, between [0, 100] (will be clipped to F_THRUSTER_MAX_V)
                                   # use_thruster == 2  %, desired % of F_THRUSTER_MAX_V, between [0, 100] 
                                   # 3  N/A for this behavior
                                   # use_thruster == 4  watt, desired input power, between [1, 9] Watts 

    b_arg: enable_steering(bool) 1  # Enable or disable steering while hovering. 
                                   # Set to True if goto_list or set_heading are to be used.


    	# Arguments for dive_to when diving to hover zone
    b_arg: d_use_bpump(enum)       2
    b_arg: d_bpump_value(X)   -260.0
    b_arg: d_use_pitch(enum)       3  # servo on pitch
    b_arg: d_pitch_value(X)  -0.4538  # -26 degrees

    	# Arguments for climb_to when climbing to hover zone
    	# As we are actually diving to the hover zone, most likely the climb will not be utilized.
    	# Instead, drift-at-depth will deactivate after the stop_when_hover_for time elapses, from 
    	# which the surface behavior will take over.
    b_arg: c_use_bpump(enum)       2
    b_arg: c_bpump_value(X)   260.0
    b_arg: c_use_pitch(enum)       3  # servo on pitch
    b_arg: c_pitch_value(X)   0.4538  # 26 degrees

    b_arg: battpos_db(nodim) 0.2 # How much to scale battpos deadband, f_battpos_db_frac_dz   

<end:b_arg>
# NOTE: These are symbolically defined beh_args.h
# b_arg: START_WHEN     When the behavior should start, i.e. go from UNITIALIZED to ACTIVE
#    BAW_IMMEDIATELY    0   // immediately
#    BAW_STK_IDLE       1   // When stack is idle (nothing is being commanded)
#    BAW_PITCH_IDLE     2   // When pitch is idle(nothing is being commanded)
#    BAW_HEADING_IDLE   3   // When heading is idle(nothing is being commanded)
#    BAW_UPDWN_IDLE     4   // When bpump/threng is idle(nothing is being commanded)
#    BAW_NEVER          5   // Never stop
#    BAW_WHEN_SECS      6   // After behavior arg "when_secs", from prior END if cycling
#    BAW_WHEN_WPT_DIST  7   // When sensor(m_dist_to_wpt) < behavior arg "when_wpt_dist"
#    BAW_WHEN_HIT_WAYPOINT 8 // When X_HIT_A_WAYPOINT is set by goto_wpt behavior
#    BAW_EVERY_SECS     9   // After behavior arg "when_secs", from prior START if cycling
#    BAW_EVERY_SECS_UPDWN_IDLE 10  // After behavior arg "when_secs", from prior START AND
#                                  //       updown is idle, no one commanding vertical motion
#    BAW_SCI_SURFACE    11  // SCI_WANTS_SURFACE is non-zero
#    BAW_NOCOMM_SECS    12  // when have not had comms for WHEN_SECS secs
#
# b_arg: STOP_WHEN
#   0   complete
#   1-N same as "start_when"
