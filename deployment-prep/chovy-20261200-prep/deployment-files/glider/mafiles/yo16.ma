behavior_name=yo
# yo16.ma
# Uses constant thruster at 4W on dive and climb
# climb 3m   dive 12m alt 5m pitch 26 deg
# 2014-09-30 lacooney@alum.mit.edu Initial, copied from yo10.ma
# 2015-08-21 lacooney@alum.mit.edu Added items to uncomment for shallow pitch mission, M#2327
<start:b_arg>
    b_arg: start_when(enum)      2   # pitch idle (see doco below)
    b_arg: num_half_cycles_to_do(nodim) -1   # Number of dive/climbs to perform
                                     # <0 is infinite, i.e. never finishes

    # arguments for dive_to
    b_arg: d_target_depth(m)     12
    b_arg: d_target_altitude(m)   5
# Uncomment and replace above values for shallow pitch mission
#    b_arg: d_target_depth(m)     100
#    b_arg: d_target_altitude(m)   30

    b_arg: d_use_pitch(enum)      3   # 1:battpos  2:setonce  3:servo
                                      #   in         rad        rad, <0 dive
    b_arg: d_pitch_value(X)   -0.4538     # -26 deg
# Uncomment and replace above value for shallow pitch mission
#        b_arg: d_pitch_value(X)   -0.209     # -12 deg

    b_arg: d_use_thruster(enum)   4  # 4  Command input power. See sensors for use_thruster = power	
    b_arg: d_thruster_value(X)   4 # use_thruster == 4  watt, desired input power, between [3, 9] Watts 

# Uncomment for shallow pitch mission
#    b_arg: d_stop_when_hover_for(sec) 3600.0        # set larger than dive time to avoid triggering
#    b_arg: d_stop_when_stalled_for(sec) 3600.0      # set larger than dive time to avoid triggering

    # arguments for climb_to
    b_arg: c_target_depth(m)      3
    b_arg: c_target_altitude(m)  -1

    b_arg: c_use_pitch(enum)      3   # 1:battpos  2:setonce  3:servo
                                      #   in         rad        rad, >0 climb
    b_arg: c_pitch_value(X)     0.4538     # 26 deg 
# Uncomment and replace above value for shallow pitch mission
#    b_arg: c_pitch_value(X)     0.209     # 12 deg

    b_arg: c_use_thruster(enum)   4 # 4  Command input power. See sensors for use_thruster = power
    b_arg: c_thruster_value(X)   4 # use_thruster == 4  watt, desired input power, between [1, 9] Watts 

# Uncomment for shallow pitch mission
#    b_arg: c_stop_when_hover_for(sec) 3600.0        # set larger than climb time to avoid triggering
#    b_arg: c_stop_when_stalled_for(sec) 3600.0      # set larger than climb time to avoid triggering
    b_arg: end_action(enum) 2     # 0-quit, 2 resume
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
