# config.sci
# Generic version
# Used to specify which sensors are sent to the glider and when
#
# 07-Jan-02 tc@DinkumSoftware.com Just the ping variable
# 23-oct-02 trcrawford@malvernsoft.com ctd controller c_profile_on
# 31-oct-02 trcrawford@malvernsoft.com hs2 controller c_hs2_on

# Send over the ping variable
sensor: x_ping_glider_to_sci  ALWAYS

# the ctd controller
sensor: c_profile_on ALWAYS

# the hs2 controller
sensor: c_hs2_on ALWAYS

