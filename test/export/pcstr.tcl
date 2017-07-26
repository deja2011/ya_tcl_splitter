source -echo -verbose CONSTRAINT/scripts/source_3.pcstr.tcl
## MA  INFO : Command remove_attribute is translated to MA_remove_attribute. (MA-001)
MA_remove_attribute [get_lib_cells RV40FTMH_Pss_*/*SDFF*U] dont_use
## MA  INFO : Command remove_attribute for attribute dont_touch is translated to set_dont_touch. (MA-042)
set_dont_touch [get_lib_cells RV40FTMH_Pss_*/*SDFF*U] false
