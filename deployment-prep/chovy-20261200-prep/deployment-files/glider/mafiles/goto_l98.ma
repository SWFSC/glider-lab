behavior_name=goto_list
#  Written by GLMPC
# 2018-07-23 lcooney@teledyne.com Initial
# Used by under ice mission recov.mi, replace with your own appropriate waypoints for a 'safe' ice-free location
# goto_l98.ma

<start:b_arg>
b_arg: start_when(enum) 0
b_arg: list_stop_when(enum) 007
b_arg: initial_wpt(enum) -2
b_arg: num_legs_to_run(nodim) -1
b_arg: num_waypoints(nodim) 2
<end:b_arg>
<start:waypoints>
-7032.0640   4138.1060
-7031.9200   4138.1090
<end:waypoints>
