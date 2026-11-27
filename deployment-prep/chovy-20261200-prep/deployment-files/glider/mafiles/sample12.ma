behavior_name=sample
# sample all science sensors on dive/hover/climb
# 2013-Apr-24 lacooney@alum.mit.edu Modified from sample10.ma

<start:b_arg>
   b_arg: sensor_type(enum)                 0 # ALL	    	0  C_SCIENCE_ALL_ON
                                              # PROFILE     1  C_PROFILE_ON
                                              # HS2	    	2  C_HS2_ON       !!DELETED!!
                                              # BB2F	    3  C_BB2F_ON
                                              # BB2C	    4  C_BB2C_ON
                                              # BB2LSS      5  C_BB2LSS_ON
                                              # SAM	    	6  C_SAM_ON
                                              # WHPAR       7  C_WHPAR_ON     !!DELETED!!
                                              # WHGPBM      8  C_WHGPBM_ON    !!DELETED!!
                                              # MOTEOPD     9  C_MOTEOPD_ON
                                              # BBFL2S     10  C_BBFL2S_ON
                                              # FL3SLO     11  C_FL3SLO_ON
                                              # BB3SLO     12  C_BB3SLO_ON
                                              # OXY3835    13  C_OXY3835_ON
                                              # WHFCTD     14  C_WHFCTD_ON
                                              # BAM        15  C_BAM_ON
                                              # OCR504R    16  C_OCR504R_ON
                                              # OCR504I    17  C_OCR504I_ON
                                              # BADD       18  C_BADD_ON
                                              # FLNTU      19  C_FLNTU_ON
                                              # FL3SLOV2   20  C_FL3SLOV2_ON
                                              # BB3SLOV2   21  C_BB3SLOV2_ON
                                              # OCR507R    22  C_OCR507R_ON
                                              # OCR507I    23  C_OCR507I_ON
                                              # BB3SLOV3   24  C_BB3SLOV3_ON
                                              # BB2FLS     25  C_BB2FLS_ON
                                              # BB2FLSV2   26  C_BB2FLSV2_ON
                                              # OXY3835_WPHASE 27 C_OXY3835_WPHASE_ON
                                              # AUVB       28  C_AUVB_ON
                                              # BB2FV2     29  C_BB2FV2_ON
                                              # TARR       30  C_TARR_ON
                                              # BBFL2SV2   31  C_BBFL2SV2_ON
                                              # GLBPS      32  C_GLBPS_ON
                                              # SSCSD      33  C_SSCSD_ON
                                              # BB2FLSV3   34  C_BB2FLSV3_ON
                                              # FIRE       35  C_FIRE_ON
                                              # OHF        36  C_OHF_ON		!!DELETED!!
                                              # BB2FLSV4   37  C_BB2FLSV4_ON
                                              # BB2FLSV5   38  C_BB2FLSV5_ON
                                              # LOGGER     39  C_LOGGER_ON
                                              # BBAM       40  C_BBAM_ON
                                              # UMODEM     41  C_UMODEM_ON
                                              # RINKOII    42  C_RINKOII_ON
                                              # DVL        43  C_DVL_ON
                                              # BB2FLSV6   44  C_BB2FLSV6_ON
                                              # FLBBRH     45  C_FLBBRH_ON
                                              # FLUR       46  C_FLUR_ON
                                              # BB2FLSV7   47  C_BB2FLSV7_ON
                                              # FLBBCD     48  C_FLBBCD_ON
                                              # DMON       49  C_DMON_ON
                                              # C3SFL      50  C_C3SFL_ON
                                              # SUNA       51  C_SUNA_ON
                                              # SATPAR     52  C_SATPAR_ON
                                              # VSF        53  C_VSF_ON
                                              # OXY4       54  C_OXY4_ON
                                              # GAMMA_RAD5 55  C_GAMMA_RAD5_ON !!DELETED!!
                                              # BSIPAR     56  C_BSIPAR_ON
                                              # FLBB       57  C_FLBB_ON
                                              # VR2C       58  C_VR2C_ON
                                              # CTD41CP2   59  C_CTD41CP2_ON
                                              # ECHOSNDR853 60 C_ECHOSNDR853_ON
                                              # FLRH       61  C_FLRH_ON
                                              # BB2FLSV8   62  C_BB2FLSV8_ON
                                              # UVILUXPAH  63  C_UVILUXPAH_ON
                                              # AD2CP      64  C_AD2CP_ON
                                              # MINIPROCO2 65  C_MINIPROCO2_ON
                                              # PCO2       66  C_PCO2_ON
                                              # SEAOWL     67  C_SEAOWL_ON
											  # AZFP       68  C_AZFP_ON
                                              # UBAT       69  C_UBAT_ON
                                              # LISST      70  C_LISST_ON
                                              # LMS        71  C_LMS_ON
                                              # SVS603     72  C_SVS603_ON
                                              # MICRORIDER 73  C_MICRORIDER_ON
                                              # BB2FLSV9   74  C_BB2FLSV9_ON
                                              # SBE41N_PH  75  C_SBE41N_PH_ON
                                              # FL2URRH    76  C_FL2URRH_ON
                                              # FLBBBBV1   77  C_FLBBBBV1_ON
                                              # FLBBBBV2   78  C_FLBBBBV2_ON
                                              # OBSVR      79  C_OBSVR_ON
                                              # FL2PECDOM  80  C_FL2PECDOM_ON
                                              # WETLABSA   81  C_WETLABSA_ON
                                              # WETLABSB   82  C_WETLABSB_ON
                                              # WETLABSC   83  C_WETLABSC_ON
                                              # ECHODROID  84  C_ECHODROID_ON
                                              # TAU        85  C_TAU_ON
                                              # RBRODO     86  C_RBRODO_ON
                                              # SOLOCAM    87  C_SOLOCAM_ON
                                              # AMAR       88  C_AMAR_ON
                                              # VRO        89  C_VRO_ON
                                      
                                                # This is a bit-field, combine:
                                                # 8 on_surface, 4 climbing, 2 hovering, 1 diving
    b_arg: state_to_sample(enum)             7  # 0  none
                                                # 1  diving
                                                # 2  hovering
                                                # 3  diving|hovering
                                                # 4  climbing
                                                # 5  diving|climbing
                                                # 6  hovering|climbing
                                                # 7  diving|hovering|climbing
                                                # 8  on_surface
                                                # 9  diving|on_surface
                                                # 10 hovering|on_surface
                                                # 11 diving|hovering|on_surface
                                                # 12 climbing|on_surface
                                                # 13 diving|climbing|on_surface
                                                # 14 hovering|climbing|on_surface
                                                # 15 diving|hovering|climbing|on_surface


    b_arg: intersample_time(s)                0  # if < 0 then off, if = 0 then
                                                 # as fast as possible, and if
                                                 # > 0 then that many seconds
                                                 # between measurements

    b_arg: nth_yo_to_sample(nodim)            1  # After the first yo, sample only
                                                 # on every nth yo. If argument is
                                                 # negative then exclude first yo.

    b_arg: intersample_depth(m)              -1  # supersedes intersample_time
                                                 # by dynamically estimating
                                                 # and setting intersample_time
                                                 # to sample at the specified
                                                 # depth interval. If <=0 then
                                                 # then sample uses
                                                 # intersample_time, if > 0 then
                                                 # that many meters between
                                                 # measurements

    b_arg: min_depth(m)                      -5  # minimum depth to collect data, default
                                                 # is negative to leave on at surface in
                                                 # spite of noise in depth reading
    b_arg: max_depth(m)                    2000  # maximum depth to collect data

    b_arg: tod_start(hhmm)                   -1  # Time Of Day start hhmm
                                                 # -1 disabled
                                                 # hh(00-23) mm(00-59)
    b_arg: tod_stop(hhmm)                    -1  # Time Of Day stop hhmm
                                                 # -1 disabled
                                                 # hh(00-23) mm(00-59)

<end:b_arg>
