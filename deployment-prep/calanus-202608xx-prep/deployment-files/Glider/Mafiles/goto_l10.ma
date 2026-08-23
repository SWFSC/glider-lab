behavior_name=goto_list
# Written by SFMC on UTC: 2026-08-23T22:56:56.287999543
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
-11723.46	3254.78
-11742.01	3245.52
-11800.56	3236.25
-11819.11	3226.96
-11837.66	3217.65
<end:waypoints>
