##PRS-STAGE-BEGIN: rtlscr

##PRS-ADD-STR: add dcprs_is_upf_design
set dcprs_is_upf_design 1
##PRS-ADD-END: add dcprs_is_upf_design

##PRS-ADD-STR: make up global scoped application options to fix sanity check mismatch.
# Warning: Variable mismatch: DC:  case_analysis_disable_non_dominant_arcs = false
set_app_options -as_user_default -name time.case_analysis_disable_non_dominant_arcs -value false
# Warning: Variable mismatch: DC:  case_analysis_disable_noncontrol_arcs = false
set_app_options -as_user_default -name time.case_analysis_disable_noncontrol_arcs -value false
prelude::copy fmrtl start
# Warning: Variable mismatch: DC:  *clock gating always use user setting in DC* = true
set_app_options -as_user_default -name time.clock_gating_user_setting_only -value true
prelude::copy fmrtl end
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable timing_separate_clock_gating_group is translated to application option time.use_special_default_path_groups. (MA-074)
set_app_options -as_user_default -name time.use_special_default_path_groups -value true
##PRS-ADD-END: make up global scoped application options to fix sanity check mismatch.

echo "Hello"
