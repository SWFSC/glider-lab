behavior_name=goto_list
# Written by SFMC on UTC: 2026-08-24T15:32:01.038710947
# goto_l10.ma

<start:b_arg>
	b_arg: num_legs_to_run(nodim) -1
	b_arg: start_when(enum) 0 # BAW_IMMEDIATELY
	b_arg: list_stop_when(enum) 7 # WHEN_WPT_DIST
	b_arg: list_when_wpt_dist(m) 10.0
	b_arg: initial_wpt(enum) 0
	b_arg: num_waypoints(nodim) 5
<end:b_arg>
<start:waypoints>
-11731.82	3250.66
-11748.28	3242.43
-11804.74	3234.18
-11821.2	3225.92
-11837.66	3217.65
<end:waypoints>
