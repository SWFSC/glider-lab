behavior_name=goto_list
# Written by SFMC on UTC: 2026-09-18T22:07:20.069910680
# goto_l10.ma

<start:b_arg>
	b_arg: num_legs_to_run(nodim) -1
	b_arg: start_when(enum) 0 # BAW_IMMEDIATELY
	b_arg: list_stop_when(enum) 7 # WHEN_WPT_DIST
	b_arg: list_when_wpt_dist(m) 50.0
	b_arg: initial_wpt(enum) 0
	b_arg: num_waypoints(nodim) 15
<end:b_arg>
<start:waypoints>
#  LON         LAT
-11723.55      3248.63 #Off the shelf
-11732.23      3250.70 #93.30
<end:waypoints>
