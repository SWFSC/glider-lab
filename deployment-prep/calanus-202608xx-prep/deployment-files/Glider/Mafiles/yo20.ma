behavior_name=yo
# 2022-Nov-15 ACossio stock yo20.ma used in 1k_n.mi
<start:b_arg>
    # How many half-yos to perform
    b_arg:  num_half_cycles_to_do(nodim)     2    # Number of dive/climbs to perform 


    # DIVE_TO ARGUMENTS
        # Depth Arguments
        b_arg:  d_target_depth(m)       	20    # (m) 20m to start
        b_arg:  d_target_altitude(m)    	30    # normal altitude/buffer

        # Advanced Flight Controls
            # Ballast Pump Controls
                b_arg:  d_use_bpump(enum)	0	   # 0  Autoballast/Depth rate control.  See doco/how-it-works/autoballast.txt
                                                   # 1  Reserved - do not use (uses d_bpump_value cc about 0)
                                                   # 2  Buoyancy Pump absolute (uses d_bpump_value as total difference between dive and climbs)
                                                   # 5  Speed relative to water current. See 'use_bpump=SM_WATER_SPEED' section
                b_arg:  d_bpump_value(X)    800    # 

            # Dive Angle Arguments (using AP)
                b_arg:  d_use_pitch(enum)   	3	# 4  Fluid Pumped absolute
													# 3  Servo on Pitch
													# 2  Pitch, set once from curve
													# 1  BattPos
                b_arg:  d_pitch_value(X)    -0.454  # 23 degrees 26 deg for Nortek 0.454: 23deg for AZFP 0.401


          # THRUSTER USE depth rate
            # b_arg: d_use_thruster(enum) 3  	# 0  Not in use
                                                # 1  Command input voltage (as % of glider voltage)
                                                # 2  Command input voltage (as % of max thruster input voltage)
                                                # 3  Command depth rate.  See sensors for use_thruster = depthrate
                                                # 4  Command input power. See sensors for use_thruster = power
            # b_arg: d_thruster_value(X) 0.05 	# 3 rate (m/s)
		# THRUSTER USE Watts
            # b_arg: d_use_thruster(enum) 4 	# enum 4 - specify value in Watts
            # b_arg: d_thruster_value(X) 5 		# Value in Watts

    # STUCK SCENARIO
        b_arg:  d_stop_when_stalled_for(sec)    180
        b_arg:  d_stop_when_hover_for(sec)      180


    # CLIMB_TO ARGUMENTS
        # Depth Arguments
        b_arg:  c_target_depth(m)       	5		# how far from the surface
        b_arg:  c_target_altitude(m)    	-1

        # Advanced Flight Controls
            # Ballast Pump Controls
                b_arg:  c_use_bpump(enum)    	0	# see d_use_bpump(enum) above
            	b_arg:  c_bpump_value(X)   400	    # Comment in if using autoballast for processor gliders, out for persistor gliders

            # Dive Angle Arguments (using AP)
                b_arg:  c_use_pitch(enum)	3		# see d_use_pitch(enum) above
                b_arg:  c_pitch_value(X)	0.454   #  rad 23 degrees

        # THRUSTER USE depth rate
            
            # b_arg: c_use_thruster(enum) 3 	# 3 specify depth rate
            # b_arg: c_thruster_value(X) -0.05 	# 3 rate (m/s)
			
		# THRUSTER USE watts	
            # b_arg: c_use_thruster(enum) 4 	# enum 4 - specify value in Watts
            # b_arg: c_thruster_value(X) 5 		# Value in Watts

    # STUCK SCENARIO
        b_arg:  c_stop_when_stalled_for(sec)    180
        b_arg:  c_stop_when_hover_for(sec)      180

    b_arg:  end_action(enum)                2 	# 0-quit, 1-wait for ^C quit/resume, 2-resume, 3-drift til "end_wpt_dist"
												# 4-wait for ^C once  5-wait for ^C quit on timeout
<end:b_arg>
