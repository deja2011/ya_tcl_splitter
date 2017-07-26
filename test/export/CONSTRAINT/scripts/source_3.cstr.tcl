# Descartes script translated by migration_assistant Version: 2.5.8 (Build Date: Apr 28, 2017)
# Supported DC version: DC L-2016.03
# Supported Descartes version: 2.5.8

# Note:
# This section has information on DC compatible procedures.
# Please note that sourcing these procs will enable a
# Design Compiler compatibility mode. In this mode, settings
# of certain variables and certain tool attributes may be
# altered from their defaults.
#
# A few examples are  listed below.
#    set sh_continue_on_error true
#    set_app_options -global -name design.include_physical_only_objects -value false
#
# Please refer TCL files in the DC2DCRT_UTIL_PATH path for more details.
# If you are in Descartes shell, you may run the proc
# MA_print_dc_compatibility_mode for details.

# Source special procedures provided for Descartes migration
if {[lsearch [array names env] "DC2DCRT_UTIL_PATH"] >= 0} {
    set DC2DCRT_UTIL_PATH $env(DC2DCRT_UTIL_PATH)
} elseif {$synopsys_program_name == "dcrt_shell"} {
    set DC2DCRT_UTIL_PATH ${synopsys_root}/auxx/ma/tcl
} else {
    set DC2DCRT_UTIL_PATH "/u/dcntmgr/spf_main_dcnt/image_NIGHTLY/latest/auxx/ma/tcl"
}
source ${DC2DCRT_UTIL_PATH}/dcrt_util.tcl

##PRS-MVDST-STR: move from dc.tcl to setup.tcl

### NSGK feedback from consistency checker : same setting as ICC2
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable case_analysis_propagate_through_icg is translated to application option time.case_analysis_propagate_through_icg. (MA-074)
set_app_options -as_user_default -name time.case_analysis_propagate_through_icg -value true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable timing_clock_gating_propagate_enable is translated to application option time.clock_gating_propagate_enable. (MA-074)
set_app_options -as_user_default -name time.clock_gating_propagate_enable -value true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable enable_clock_to_data_analysis is translated to application option time.enable_clock_to_data_analysis. (MA-074)
set_app_options -as_user_default -name time.enable_clock_to_data_analysis -value true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable timing_edge_specific_source_latency is translated to application option time.edge_specific_source_latency. (MA-074)
set_app_options -as_user_default -name time.edge_specific_source_latency -value true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable timing_enable_non_sequential_checks is translated to application option time.enable_non_sequential_checks. (MA-074)
set_app_options -as_user_default -name time.enable_non_sequential_checks -value true
## MA ERROR : Variable rc_degrade_min_slew_when_rd_less_than_rnet is disabled because it is not supported. (MA-272)
# set rc_degrade_min_slew_when_rd_less_than_rnet true

## set dc_shell parameter ##
## MA ERROR : Variable cache_read is disabled because it is not supported. (MA-272)
# set cache_read "./.synopsys_cache"
## MA ERROR : Variable cache_write is disabled because it is not supported. (MA-272)
# set cache_write "./.synopsys_cache"
## MA ERROR : Variable alib_library_analysis_path is disabled because it is not supported. (MA-272)
# set alib_library_analysis_path "./.alib_cache"
## MA ERROR : Variable verilogout_no_tri is disabled because it is not supported. (MA-272)
# set verilogout_no_tri true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable bus_naming_style is translated to application option design.bus_delimiters. (MA-074)
## MA  INFO : Variable value %s\[%d\] is translated to []. (MA-071)
set_app_options -as_user_default -name design.bus_delimiters -value {[]}
## MA ERROR : Variable bus_inference_style is disabled because it is not supported. (MA-272)
# set bus_inference_style "%s\[%d\]"
## MA ERROR : Variable hdlout_internal_busses is disabled because it is not supported. (MA-272)
# set hdlout_internal_busses true
## MA ERROR : Variable verilogout_show_unconnected_pins is disabled because it is not supported. (MA-272)
# set verilogout_show_unconnected_pins true
## MA ERROR : Variable verilogout_higher_designs_first is disabled because it is not supported. (MA-272)
# set verilogout_higher_designs_first true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable hdlin_mux_size_limit is translated to application option hdlin.elaborate.mux_size_limit. (MA-074)
##PRS-RM-1-STR: this application option is removed from DCRT UI.
# set_app_options -as_user_default -name hdlin.elaborate.mux_size_limit -value 256
##PRS-RM-1-END: this application option is removed from DCRT UI.
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable hdlin_latch_always_async_set_reset is translated to application option hdlin.elaborate.latch_infer_async_set_reset. (MA-074)
##PRS-ADD-2-STR: dcrt-only application options.
# set_app_options -as_user_default -name hdlin.elaborate.latch_infer_async_set_reset -value true
##PRS-ADD-2-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name hdlin.elaborate.latch_infer_async_set_reset -value true
}
##PRS-ADD-2-END: dcrt-only application options.
## MA ERROR : Variable timing_enable_multiple_clocks_per_reg is disabled because it is not supported. (MA-272)
# set timing_enable_multiple_clocks_per_reg true
## MA ERROR : Variable compile_disable_hierarchical_inverter_opt is disabled because it is not supported. (MA-272)
# set compile_disable_hierarchical_inverter_opt true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable compile_enable_register_merging is translated to application option compile.seqmap.enable_register_merging. (MA-074)
##PRS-ADD-3-STR: dcrt-only application options.
# set_app_options -as_user_default -name compile.seqmap.enable_register_merging -value false
##PRS-ADD-3-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name compile.seqmap.enable_register_merging -value false
}
##PRS-ADD-3-END: dcrt-only application options.
## MA ERROR : Variable compile_clock_gating_through_hierarchy is disabled because it is not supported. (MA-272)
# set compile_clock_gating_through_hierarchy true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable hdlin_vrlg_std is translated to application option hdlin.verilog.standard. (MA-074)
##PRS-ADD-4-STR: dcrt-only application options.
# set_app_options -as_user_default -name hdlin.verilog.standard -value 2001
##PRS-ADD-4-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name hdlin.verilog.standard -value 2001
}
##PRS-ADD-5-END: dcrt-only application options.
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable hdlin_preserve_sequential is translated to application option hdlin.elaborate.preserve_sequential. (MA-074)
##PRS-ADD-5-STR: dcrt-only application options.
# set_app_options -as_user_default -name hdlin.elaborate.preserve_sequential -value true
##PRS-ADD-5-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name hdlin.elaborate.preserve_sequential -value true
}
##PRS-ADD-1-END: dcrt-only application options.
## MA ERROR : Variable compile_timing_high_effort is disabled because it is not supported. (MA-272)
# set compile_timing_high_effort true
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Both constant and unloaded logic is propagated in Descartes when boundary optimization is globally disabled. Please use set_boundary_optimization command to selectively control boundary optimization on a specific object. (MA-647)
## MA  INFO : Variable compile_enable_constant_propagation_with_no_boundary_opt is translated to application option compile.optimization.constant_and_unloaded_propagation_with_no_boundary_optimization. (MA-074)
##PRS-ADD-6-STR: dcrt-only application options.
# set_app_options -as_user_default -name compile.optimization.constant_and_unloaded_propagation_with_no_boundary_optimization -value false
##PRS-ADD-6-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name compile.optimization.constant_and_unloaded_propagation_with_no_boundary_optimization -value false
}
##PRS-ADD-6-END: dcrt-only application options.
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable enable_recovery_removal_arcs is translated to application option time.disable_recovery_removal_checks. (MA-074)
## MA  INFO : Variable value true is translated to false. (MA-071)
set_app_options -as_user_default -name time.disable_recovery_removal_checks -value false
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable compile_delete_unloaded_sequential_cells is translated to application option compile.seqmap.remove_unloaded_registers. (MA-074)
##PRS-ADD-7-STR: dcrt-only application options.
# set_app_options -as_user_default -name compile.seqmap.remove_unloaded_registers -value false
##PRS-ADD-7-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name compile.seqmap.remove_unloaded_registers -value false
}
##PRS-ADD-7-END: dcrt-only application options.
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable compile_seqmap_propagate_constants is translated to application option compile.seqmap.remove_constant_registers. (MA-074)
##PRS-ADD-8-STR: dcrt-only application options.
# # # # # # # # # set_app_options -as_user_default -name compile.seqmap.remove_constant_registers -value false
##PRS-ADD-8-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name compile.seqmap.remove_constant_registers -value false
}
##PRS-ADD-8-END: dcrt-only application options.
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable hdlin_shorten_long_module_name is translated to application option hdlin.naming.shorten_long_module_name. (MA-074)
##PRS-ADD-9-STR: dcrt-only application options.
# set_app_options -as_user_default -name hdlin.naming.shorten_long_module_name -value true
##PRS-ADD-9-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name hdlin.naming.shorten_long_module_name -value true
}
##PRS-ADD-9-END: dcrt-only application options.
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable hdlin_module_name_limit is translated to application option hdlin.naming.module_name_limit. (MA-074)
##PRS-ADD-10-STR: dcrt-only application options.
# set_app_options -as_user_default -name hdlin.naming.module_name_limit -value 50
##PRS-ADD-10-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name hdlin.naming.module_name_limit -value 50
}
##PRS-ADD-10-END: dcrt-only application options.
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable template_naming_style is translated to application option hdlin.naming.template_naming_style. (MA-074)
##PRS-ADD-11-STR: dcrt-only application options.
# set_app_options -as_user_default -name hdlin.naming.template_naming_style -value %s
##PRS-ADD-11-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name hdlin.naming.template_naming_style -value %s
}
##PRS-ADD-11-END: dcrt-only application options.
## MA  INFO : Command set is translated to set_app_options. (MA-001)
## MA  INFO : Variable template_parameter_style is translated to application option hdlin.naming.template_parameter_style. (MA-074)
##PRS-ADD-12-STR: dcrt-only application options.
# set_app_options -as_user_default -name hdlin.naming.template_parameter_style -value %s
##PRS-ADD-12-SPLT: dcrt-only application options.
if {$synopsys_program_name == "dcrt_shell"} {
    set_app_options -as_user_default -name hdlin.naming.template_parameter_style -value %s
}
##PRS-ADD-12-END: dcrt-only application options.
### NSGK ### set placer_max_cell_density_threshold 0.80
set GCLK_AND RV40FTMH_Pss_V1p1_T170/TMHAND2CLX20
set GCLK_MUX RV40FTMH_Pss_V1p1_T170/TMHMUX2CLX20
set GCLK_ICG RV40FTMH_Pss_V1p1_T170/TMHGTDPX40
set NEW_SE_PIN XXX_GATED_CLOCK_HOOKUP_TEST_PORT_DUMMY_NAME_XXX
set VERISYN_LATCH X4515
## MA ERROR : Variable compile_clock_gating_through_hierarchy is disabled because it is not supported. (MA-272)
# set compile_clock_gating_through_hierarchy true
set pwr_global_check_boundary_opto false

##PRS-STAGE-END: cstr
