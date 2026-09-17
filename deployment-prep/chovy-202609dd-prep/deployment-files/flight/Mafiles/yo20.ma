behavior_name=yo

# yo20.ma
# define number of yos, dive depth, climb depth, 
# Basic parameters for Autoballast routine to reduce total drive to d_bpump_value
# with minimum vertical speed d_speed_min and c_speed_min
# See /doco/how-it-works/autoballast.txt and masterdata for full list of b_args.


<start:b_arg>
    b_arg: start_when(enum)              2 # pitch idle (see doco below)
    b_arg: num_half_cycles_to_do(nodim)  2 # Number of dive/climbs to perform
					   # <0 is infinite, i.e. never finishes
					   # 2 half cycles = 1 yo
 # Arguments for dive_to
    b_arg: d_target_depth(m)    20	   # depth the glider will dive to
    b_arg: d_target_altitude(m)  50        # how far off the bottom to turn around

   ## Pump arguments
    b_arg: d_use_bpump(enum)    0 # 0  Autoballast/Speed control.

    b_arg: d_bpump_value(X)   400 # use_bpump == 0   Total amt of ballast.  Stored as C_AUTOBALLAST_VOLUME 
				  # use_bpump == 2   cc, clips to max legal  >0 goes up
   ## Pitch arguments
    b_arg: d_use_pitch(enum)      3 # 1:battpos  2:setonce  3:servo (auto-pitch)
				    #   in         rad        rad, <0 dive
    b_arg: d_pitch_value(X) -0.4538 # -26 deg = -0.4538 rad;

   ## Speed control arguments
    b_arg: d_stop_when_hover_for(sec)   600.0 # increased to accomodate slower depth rate for autoballast
    b_arg: d_stop_when_stalled_for(sec) 660.0 # increased to accomodate slower depth rate for autoballast
    b_arg: d_speed_min(m/s)              0.06 # minimum depth rate for dive

   ## Thruster Arguments
  # b_arg: d_use_thruster(enum) 4 	# enum 4 - specify value in Watts
  # b_arg: d_thruster_value(X) 5 	# Value in Watts


 # Arguments for climb_to
    b_arg: c_target_depth(m)      7
    b_arg: c_target_altitude(m)  -1

   ## Pump arguments
    b_arg: c_use_bpump(enum)     0  # 0  Autoballast/Speed control.

   ## Pitch arguments
    b_arg: c_use_pitch(enum)     3  # 1:battpos  2:setonce  3:servo (auto-pitch)
				    #   in         rad        rad, >0 climb
    b_arg: c_pitch_value(X) 0.4538  # 26 deg =  0.4538 rad;

   ## Speed control arguments
    b_arg: c_stop_when_hover_for(sec)   600.0 # increased to accomodate slower depth rate for autoballast
    b_arg: c_stop_when_stalled_for(sec) 660.0 # increased to accomodate slower depth rate for autoballast
    b_arg: c_speed_min(m/s)             -0.06 # minimum depth rate for climb

   ## Thruster Arguments
  # b_arg: c_use_thruster(enum) 4 	# enum 4 - specify value in Watts
  # b_arg: c_thruster_value(X) 5 	# Value in Watts


    b_arg: end_action(enum)                 2 # 0-quit, 2 resume
<end:b_arg>
