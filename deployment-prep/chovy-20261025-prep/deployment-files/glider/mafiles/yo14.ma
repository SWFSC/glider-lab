behavior_name=yo
# yo14.ma
# climb 7m   dive 30m alt 9m pitch 26 deg
# Basic parameters for Autoballast routine to reduce total drive to d_bpump_value
# with minimum vertical speed d_speed_min and c_speed_min
# See /doco/how-it-works/autoballast.txt and masterdata for full list of b_args.
# 2011-09-19 lcooney@teledyne.com Initial, copied from yo10.ma
# 2016-02-04 lcooney@teledyne.com Added d/c_stop_when_hover/stalled_for args, M#2632
# 2017-08-24 lcooney@teledyne.com Changed speed_min to 0.06, increased altitude from 3->5

<start:b_arg>
    b_arg: start_when(enum)      2   # pitch idle (see doco below)
    b_arg: num_half_cycles_to_do(nodim) -1   # Number of dive/climbs to perform
                                     # <0 is infinite, i.e. never finishes

    # arguments for dive_to
    b_arg: d_target_depth(m)     30
    b_arg: d_target_altitude(m)   5

    b_arg: d_use_bpump(enum) 0     # 0  Autoballast/Speed control.  
    b_arg: d_bpump_value(X) 300.0 # use_bpump == 0   Total amt of ballast, stored as C_AUTOBALLAST_VOLUME

    b_arg: d_use_pitch(enum)      3   # 1:battpos  2:setonce  3:servo
                                      #   in         rad        rad, <0 dive
    b_arg: d_pitch_value(X)   -0.4538     # -26 deg
    b_arg: d_stop_when_hover_for(sec) 600.0        # increased to accomodate slower depth rate for autoballast 
    b_arg: d_stop_when_stalled_for(sec) 660.0      # increased to accomodate slower depth rate for autoballast 
    b_arg: d_speed_min(m/s) 0.06      # minimum depth rate for dive


    # arguments for climb_to
    b_arg: c_target_depth(m)      7
    b_arg: c_target_altitude(m)  -1

    b_arg: c_use_bpump(enum) 0	  # 0  Autoballast/Speed control. 

    b_arg: c_use_pitch(enum)      3   # 1:battpos  2:setonce  3:servo
                                      #   in         rad        rad, >0 climb
    b_arg: c_pitch_value(X)     0.4538     # 26 deg
    b_arg: c_stop_when_hover_for(sec) 600.0        # increased to accomodate slower depth rate for autoballast 
    b_arg: c_stop_when_stalled_for(sec) 660.0        # increased to accomodate slower depth rate for autoballast 
    b_arg: c_speed_min(m/s) -0.06      # minimum depth rate for climb

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
