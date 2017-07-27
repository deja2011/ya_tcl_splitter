# place.coarse.max_density                                                             float   --        0.8              0                  block normal
set_app_options -name place.coarse.max_density -value 0.8
# time.case_analysis_propagate_through_icg                                             bool    --        true             false              block normal
set_app_options -name time.case_analysis_propagate_through_icg -value true
# time.enable_clock_to_data_analysis                                                   bool    --        true             false              block normal
set_app_options -name time.enable_clock_to_data_analysis -value true
# time.port_slew_derate_from_library                                                   float   --        0.5              1                  block normal
set_app_options -name time.port_slew_derate_from_library -value 0.5
# time.port_slew_lower_threshold_fall                                                  float   --        30               20                 block normal
source -echo -verbose CONSTRAINT/scripts/source_2.setup.tcl
