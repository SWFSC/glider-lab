behavior_name=goto_list
# Written by SFMC on UTC: 2026-10-16T18:51:00.591298702
# goto_l10.ma

<start:b_arg>
	b_arg: num_legs_to_run(nodim) -1
	b_arg: start_when(enum) 0 # BAW_IMMEDIATELY
	b_arg: list_stop_when(enum) 7 # WHEN_WPT_DIST
	b_arg: list_when_wpt_dist(m) 1000.0
	b_arg: initial_wpt(enum) -1
	b_arg: num_waypoints(nodim) 10
<end:b_arg>
<start:waypoints>
-12420.5	4104.0	#0 TH03
-12426.0	4104.0	#1 TH04
-12435.0	4104.0	#2 TH05
-12445.0	4104.0	#3 TH06
-12456.0	4104.0	#4 TH07
-12506.0	4104.0	#5 offshore
-12456.01	4104.0	#6 TH07
-12445.01	4104.0	#7 TH06
-12435.01	4104.0	#8 TH05
-12426.01	4104.0	#9 TH04
<end:waypoints>
