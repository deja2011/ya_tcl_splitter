#!/usr/bin/env python3
# coding=utf-8

"""
Build PRS directory from run directory of original testcase, with prelude enabled.
"""


import argparse
from os.path import isdir
import shutil

from source_tree import Flow


def split_scripts(source_tree_file, separator_file, mapping_file, output_dir, force=False):
    """
    Split Tcl scripts and export to designated directory.
    """
    if isdir(output_dir) and force:
        shutil.rmtree(output_dir)
    flow = Flow(source_tree_file=source_tree_file,
                separator_file=separator_file,
                mapping_file=mapping_file)
    flow.split_all()
    flow.build_all(output_dir)
    flow.move_top_scripts(output_dir)


def main():
    """
    main function for argument parsing.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--source_tree',
                        help="specify path to source tree file.",
                        required=True)
    parser.add_argument('-s', '--separators',
                        help="specify path to separators file.",
                        required=True)
    parser.add_argument('-m', '--mapping',
                        help="specify path to path mapping file.",
                        required=True)
    parser.add_argument('-o', '--output',
                        help="specify path to output directory. "
                        "Output directory is equivalent to DCRT_user_data "
                        "or DC_user_data",
                        required=True)
    parser.add_argument('-f', '--force', action='store_true',
                        help="force to remove output directory if it exists.")
    args = parser.parse_args()
    split_scripts(source_tree_file=args.source_tree,
                  separator_file=args.separators,
                  mapping_file=args.mapping,
                  output_dir=args.output,
                  force=args.force)


if __name__ == "__main__":
    main()
