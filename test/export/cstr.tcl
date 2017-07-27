##PRS-STAGE-BEGIN: cstr

foreach_in_collection lib_cell_tmp [get_lib_cells RV40FTMH_Pss_*/*SDFF* -filter "name !~ *SDFF*U"] {
    ## MA  INFO : Command set_dont_use is translated to MA_set_dont_use. (MA-001)
    ## MA  WARN : The command set_lib_cell_purpose must be executed after the design is read in Descartes. Please move this command if necessary. (MA-604)
    MA_set_dont_use $lib_cell_tmp
    set_dont_touch $lib_cell_tmp
}
source -echo -verbose CONSTRAINT/scripts/source_3.cstr.tcl
