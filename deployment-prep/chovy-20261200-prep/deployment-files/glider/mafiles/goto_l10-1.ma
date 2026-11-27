behavior_name=goto_list
# Written by SFMC on UTC: 2026-11-17T17:26:13.657781493
# goto_l10.ma

<start:b_arg>
	b_arg: num_legs_to_run(nodim) -1
	b_arg: start_when(enum) 0 # BAW_IMMEDIATELY
	b_arg: list_stop_when(enum) 7 # WHEN_WPT_DIST
	b_arg: list_when_wpt_dist(m) 1000.0
	b_arg: initial_wpt(enum) 0
	b_arg: num_waypoints(nodim) 3
<end:b_arg>
<start:waypoints>
-12435.0	4104.0	#0 TH05
-12434.8	4050.8	#1 south
-12428.5	4050.5	#2 inshore
<end:waypoints>
