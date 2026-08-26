behavior_name=surface

# SURFAC40.MA (No Comms)
# short no comms file
# 2022-Nov-15 ACossio stock surfac40.ma used in 1k_n.mi

<start:b_arg>

      b_arg: start_when(enum)         12  # 12 No comms
 # Surface for no comms (file transfer uncompleted)
        b_arg:  when_secs(sec)           28800   # 8 hours

 # Surface Timeouts & Other Params
        		
	b_arg: report_all(bool)             0       #  T->report all sensors once, F->just gps
        b_arg: end_action(enum)             1       # 0-quit, 1-wait for ^C quit/resume, 2-resume, 3-drift til "end_wpt_dist"
													# 4-wait for ^C once  5-wait for ^C quit on timeout
        b_arg: gps_wait_time(sec)           300     # 5 minutes how long to wait for gps
        b_arg: keystroke_wait_time(sec)     599     # 10 minutes how long to wait for control-C
        b_arg: printout_cycle_time(sec)     30.0    # How often to print dialog
		b_arg: gps_postfix_wait_time(sec) 	16.0    # How long to wait after initial
													# gps fix before turning the iridium
													# on (which disables the gps).  It will
													# wait the shorter of this time or until
													# all the water velocity calculations are
													# complete.
   

   # Climb arguments when this surface behavior becomes active 
   ## Pump arguments
    b_arg: c_use_bpump(enum)        0             # use autoballast on surface climb (requires autoballast yo)

   ## Pitch arguments
    b_arg: c_use_pitch(enum)        3             # 3:servo
    b_arg: c_pitch_value(X)         0.4538        # 26 deg
        
   
<end:b_arg>