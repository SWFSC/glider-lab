behavior_name=sample
# sample all science sensors on down cast only
# Sample ctd only on downcast
# sensor c_science_all_on_enabled set to 0 to uncouple all science
# see sample10.ma for complete lists and definitions
# duplicate this sample and change sensor_type to dictate sampling of other sensors
# 10-July-2010 ballsup@webbresearch.com handwritten for stock.mi
#<start:b_arg>
#    b_arg: sensor_type(enum)             1  # PROFILE (ctd)    1  C_PROFILE_ON                     
#    b_arg: state_to_sample(enum)         1  # 1  diving                                        
#    b_arg: intersample_time(s)           0  #as fast as possible
#    b_arg: nth_yo_to_sample(nodim)       1  # After the first yo                                    
#    b_arg: intersample_depth(m)         -1  # supersedes intersample_time                              
#    b_arg: min_depth(m)                 -5  # minimum depth to collect data,
#    b_arg: max_depth(m)               2000  # maximum depth to collect data
#<end:b_arg>
