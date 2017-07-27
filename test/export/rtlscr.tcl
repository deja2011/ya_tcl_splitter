source -echo -verbose CONSTRAINT/scripts/source_2.rtlscr.tcl
set_app_options -name time.port_slew_lower_threshold_fall -value 20
# time.port_slew_lower_threshold_rise                                                  float   --        30               20                 block normal
set_app_options -name time.port_slew_lower_threshold_rise -value 20
# time.port_slew_upper_threshold_fall                                                  float   --        70               80                 block normal
set_app_options -name time.port_slew_upper_threshold_fall -value 80
# time.port_slew_upper_threshold_rise                                                  float   --        70               80                 block normal
set_app_options -name time.port_slew_upper_threshold_rise -value 80
##PRS-ADD-1-END: make up block scoped application options to fix sanity check mismatch.

##PRS-STAGE-END: rtlscr
