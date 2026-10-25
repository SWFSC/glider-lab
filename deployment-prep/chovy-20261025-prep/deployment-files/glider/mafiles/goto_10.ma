behavior_name=goto_list
#  Written by gen-goto-list-ma ver 1.0 on GMT:Tue Feb 19 18:56:54 2002
#  07-Aug-02 tc@DinkumSoftware.com Manually edited for spawars 7aug02 op in buzzards bay
#  07-Aug-02 tc@DinkumSoftware.com Changed from decimal degrees to degrees, minutes, decimal minutes
#  ??-Apr-03 kniewiad@webbresearch.com changed to ashument
#  17-Apr-03 tc@DinkumSoftware.com fixed comments

# goto_l10.ma
# Flies the box in ashumet
# Each leg about 200m

<start:b_arg>
b_arg: num_legs_to_run(nodim) -1 # loop
b_arg: start_when(enum) 0 # BAW_IMMEDIATELY
b_arg: list_stop_when(enum) 7 # BAW_WHEN_WPT_DIST
b_arg: initial_wpt(enum) -2 # closest
b_arg: num_waypoints(nodim) 4
<end:b_arg>
<start:waypoints>
-7032.0640   4138.1060
-7031.9200   4138.1090
-7031.9170   4138.0000
-7032.0610   4137.9980
<end:waypoints>

