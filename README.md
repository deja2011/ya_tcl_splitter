## Overview

Tcl splitter helps to split a standalone Tcl flow into several stages.

## User Guide

Need three files be prepared in advance.

#### Source tree file

Source tree file defines which is the top script of the full flow, and how other scripts are sourced in the flow. All path values must be absolute paths. Normalized path values are recommended.

#### Separator file

Separator file defines all the position and stage information of all separators.

#### Mapping file

Mapping file defines how the split scripts are placed in output directory.

#### Usage

```
usage: split_scripts.py [-h] -t SOURCE_TREE -s SEPARATORS -m MAPPING -o OUTPUT
                        [-f]

optional arguments:
  -h, --help            show this help message and exit
  -t SOURCE_TREE, --source_tree SOURCE_TREE
                        specify path to source tree file.
  -s SEPARATORS, --separators SEPARATORS
                        specify path to separators file.
  -m MAPPING, --mapping MAPPING
                        specify path to path mapping file.
  -o OUTPUT, --output OUTPUT
                        specify path to output directory. Output directory is
                        equivalent to DCRT_user_data or DC_user_data
  -f, --force           force to remove output directory if it exists.
```

#### Example

```
split_scripts.py \
    -t test/split.source_tree.txt \
    -s test/split.5.separators.txt \
    -m test/split.mapping.txt \
    -o export \
    -f
```

#### Unit Test

```
./update_testcases.sh
python3 source_tree.py
```
