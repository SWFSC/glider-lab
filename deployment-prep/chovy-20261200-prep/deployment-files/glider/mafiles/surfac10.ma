behavior_name=surface

# SURFAC10.MA (Flight Controls) (Surface timeouts & params)
# 2022-Nov-15 ACossio stock surfac10.ma used in 1k_n.mi

<start:b_arg>
    # Flight Controls
        b_arg:  c_use_bpump(enum)       2		# 0  Autoballast/Depth rate control.  See doco/how-it-works/autoballast.txt
												# 2  Buoyancy Pump absolute (uses c_bpump_value as total difference between dive and climbs)
        b_arg:  c_bpump_value(X)        1000  	# use_bpump == 0: c_bpump_value is ignored.
												# use_bpump == 2   cc, clips to max legal  >0 goes up
        b_arg:  c_use_pitch(enum)       3       # 4  Fluid Pumped absolute
												# 3  Servo on Pitch
												# 2  Pitch, set once from curve
												# 1  BattPos
        b_arg:  c_pitch_value(X)        0.401   # 23 degrees
        
    # Surface Timeouts & Other Params
        b_arg: report_all(bool)             0       #  T->report all sensors once, F->just gps
        b_arg: end_action(enum)             1       # 0-quit, 1-wait for ^C quit/resume, 2-resume, 3-drift til "end_wpt_dist"
													# 4-wait for ^C once  5-wait for ^C quit on timeout
        b_arg: gps_wait_time(sec)           300     # 5 minutes how long to wait for gps
        b_arg: keystroke_wait_time(sec)     300     # 5 minutes how long to wait for control-C
        b_arg: printout_cycle_time(sec)     40.0    # How often to print dialog
		b_arg: gps_postfix_wait_time(sec) 	16.0    # How long to wait after initial
													# gps fix before turning the iridium
													# on (which disables the gps).  It will
													# wait the shorter of this time or until
													# all the water velocity calculations are
													# complete.
<end:b_arg>