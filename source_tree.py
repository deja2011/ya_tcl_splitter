# coding=utf-8

"""
Data structure of script source tree.
"""


import re
import sys
# import os
import io
from os import makedirs
from os.path import basename, dirname, isfile, isdir
from os.path import join as opjoin
import linecache
import unittest
from itertools import count
import shutil

import settings


def get_num_lines(file_name):
    """
    Get number of lines in a text file via a naive iteration.
    """
    i = 0
    fid = open(file_name)
    for i, _ in enumerate(fid):
        pass
    fid.close()
    return i + 1



class Separator(object):
    """
    Data structure of a separator.
    """

    def __init__(self, *args):
        if len(args) < 4:
            raise ValueError("Invalid input from separator file:\n  {}".format(
                ' '.join(args)))
        last_stage, next_stage, line_num, file_name = args[:4]
        self._last_stage = last_stage
        self._next_stage = next_stage
        self._line_num = int(line_num)
        if not isfile(file_name):
            raise ValueError("Invalid input from separator file. Cannot find"
                             "file {}:"
                             "\n  {}".format(file_name, ' '.join(args)))
        self._file_name = file_name


    @property
    def last_stage(self):
        """
        Stage property of a separator.
        Must be a choice from STAGE in settings.
        """
        return self._last_stage


    @last_stage.setter
    def last_stage(self, value):
        if value not in settings.STAGES:
            raise ValueError("Invalid stage name {}: must be one of {}".format(
                value, ", ".join(settings.STAGES)))
        self._last_stage = value


    @property
    def next_stage(self):
        """
        Stage property of a separator.
        Must be a choice from STAGE in settings.
        """
        return self._next_stage


    @next_stage.setter
    def next_stage(self, value):
        if value not in settings.STAGES:
            raise ValueError("Invalid stage name {}: must be one of {}".format(
                value, ", ".join(settings.STAGES)))
        self._next_stage = value


    @property
    def line_num(self):
        """
        Line number property of a separator.
        """
        return self._line_num


    @line_num.setter
    def line_num(self, value):
        if isinstance(value, int) and \
                1 <= value <= get_num_lines(self.file_name):
            self._line_num = value
        else:
            raise ValueError("Invalid value of separator line num."
                             "It must be a positive integer within file length.")


    @property
    def file_name(self):
        """
        File name property of a separator.
        """
        return self._file_name


    @file_name.setter
    def file_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid value on RHS. Must be a path string.")
        self._file_name = value



class Node(object):
    """
    Data structure of a Tcl script.
    """

    def __init__(self, orig_file, parent=None, line_num=0):
        self.orig_file = orig_file
        if isfile(orig_file):
            self.scope = [1, get_num_lines(self.orig_file)]
        else:
            self.scope = [0, 0]
        self.parent = parent
        self.line_num = line_num
        self.childs = list()
        self._stage = None
        self.target_dir = ''
        self.rel_dir = ''
        self.first_line = "ORIG"
        self.last_line = "ORIG"


    @property
    def stage(self):
        """
        Stage name property of a node.
        Must be a choice from STAGE in settings.
        """
        return self._stage


    @stage.setter
    def stage(self, value):
        if value not in settings.STAGES:
            raise ValueError("Invalid stage name {}: must be one of {}".format(
                value, ", ".join(settings.STAGES)))
        self._stage = value


    @property
    def target_file(self):
        """
        Query command of target file name.
        """
        if self.stage:
            segments = basename(self.orig_file).split(".")
            segments.insert(-1, self.stage)
            target_file = opjoin(dirname(self.orig_file), ".".join(segments))
        else:
            target_file = self.orig_file
        if self.target_dir:
            target_file = opjoin(self.target_dir, basename(target_file))
        return target_file


    @property
    def rel_file(self):
        """
        Query command of relative file name. Relative file name is used when
        rendering script names in source commands.
        """
        if self.stage:
            segments = basename(self.orig_file).split(".")
            segments.insert(-1, self.stage)
            rel_file = opjoin(dirname(self.orig_file), ".".join(segments))
        else:
            rel_file = self.orig_file
        if self.target_dir:
            rel_file = opjoin(self.rel_dir, basename(rel_file))
        return rel_file



    def add_child_node(self, child_node, line_num, prepend=False):
        """
        Add an existing node to current node's childs.
        """
        child_node.parent = self
        child_node.line_num = line_num
        if prepend:
            self.childs.insert(0, (line_num, child_node))
        else:
            self.childs.append((line_num, child_node))
        return child_node


    def parse(self, source_tree_file, unit_indents=2):
        """
        Parse a source tree file. Source tree file is generated by
        prelude::start_track_source
        """
        pattern = re.compile(r'^(\s*)(\d+) (\S+)\n$')
        with open(source_tree_file, "r") as fin:
            self.orig_file = next(fin).strip()
            current_node = self
            current_indents = -1
            for line in fin:
                match = re.match(pattern, line)
                if not match:
                    raise ValueError("Invalid input line in source tree file.\n"
                                     "  {}".format(line[:-1]))
                indents, line_num, file_name = match.groups()
                indents = len(indents) // unit_indents
                line_num = int(line_num)
                if current_indents == indents - 2:
                    current_node = current_node.childs[-1][-1]
                    current_node.add_child_node(Node(orig_file=file_name),
                                                line_num=line_num)
                    current_indents += 1
                elif current_indents == indents - 1:
                    current_node.add_child_node(Node(orig_file=file_name),
                                                line_num=line_num)
                elif current_indents == indents:
                    current_node = current_node.parent
                    current_node.add_child_node(Node(orig_file=file_name),
                                                line_num=line_num)
                else:
                    for _ in range(current_indents - indents + 1):
                        current_node = current_node.parent
                    current_node.add_child_node(Node(orig_file=file_name),
                                                line_num=line_num)
                    current_indents = indents - 1


    def iter_dfs(self):
        """
        A Depth-First-Search to iterate all nodes from self.
        Child nodes are ordered by the order in parent node's childs list.
        """
        stack = [(0, self)]
        while stack:
            _, node = stack.pop()
            stack.extend(reversed(node.childs))
            yield node


    def export_source_tree(self,
                           unit_indents=2,
                           fout=sys.stdout,
                           verbose=False):
        """
        Show content of a node.
        """
        stack = [(-1, 0, self), ]
        if verbose:
            fout.write("{target_file}\n"
                       "-> orig file : {orig_file}\n"
                       "-> scope : {scope}\n"
                       "-> first line : {first_line}\n"
                       "-> last line : {last_line}\n"
                       "----------------\n".format(
                           orig_file=self.orig_file,
                           target_file=self.target_file,
                           scope=self.scope,
                           first_line=self.first_line,
                           last_line=self.last_line))
        else:
            fout.write("{}\n".format(self.target_file))
        while stack:
            indents, line_num, node = stack.pop()
            stack.extend([(indents + 1, t[0], t[1])
                          for t in reversed(node.childs)])
            if indents == -1:
                continue
            if verbose:
                fout.write("{indent}{target_file}\n"
                           "{indent}-> sourced at : {line_num}\n"
                           "{indent}-> orig file : {orig_file}\n"
                           "{indent}-> scope : {scope}\n"
                           "{indent}-> first line : {first_line}\n"
                           "{indent}-> last line : {last_line}\n"
                           "----------------\n".format(
                               indent=" "*(unit_indents*(indents+1)),
                               line_num=line_num,
                               orig_file=node.orig_file,
                               target_file=node.target_file,
                               scope=node.scope,
                               first_line=node.first_line,
                               last_line=node.last_line))
            else:
                fout.write("{}{} {}\n".format(" "*(unit_indents*indents),
                                              line_num,
                                              node.target_file))


    def split_bot_up(self, last_stage, next_stage, line_num, left_child, right_child):
        """
        :type separator: Separator
        :rtype left_node: Node
        :rtype right_node: Node
        ----
        Recursively split scripts on a source chain in a bottom-up manner.
        """
        # Implement left node, link left node and left child node.
        left_node = Node(orig_file=self.orig_file)
        left_node.stage = last_stage
        left_node.scope = [self.scope[0], line_num + self.scope[0] -1]
        left_node.childs = [t for t in self.childs if t[0] < line_num]
        left_node.first_line = self.first_line
        for _, child_node in left_node.childs:
            child_node.parent = left_node
        if left_child:
            left_node.add_child_node(left_child, line_num)
            left_node.last_line = "SOURCE"
        else:
            left_node.last_line = "SPLIT {} {}".format(last_stage,
                                                       next_stage)
        # Implement right node, link right node and right child node.
        right_node = Node(orig_file=self.orig_file)
        right_node.stage = next_stage
        right_node.scope = [line_num + self.scope[0] - 1, self.scope[1]]
        right_node.childs = [(t[0] - (line_num - 1), t[1]) for t in self.childs
                             if t[0] > line_num]
        right_node.last_line = self.last_line
        for _, child_node in right_node.childs:
            child_node.parent = right_node
            child_node.line_num -= (line_num - 1)
        if right_child:
            right_node.add_child_node(right_child, 1, prepend=True)
            right_node.first_line = "SOURCE"
        else:
            right_node.first_line = "SPLIT {} {}".format(last_stage,
                                                         next_stage)
        # Recursively split parent node unless current node is the top one.
        if self.parent:
            return self.parent.split_bot_up(last_stage=last_stage,
                                            next_stage=next_stage,
                                            line_num=self.line_num,
                                            left_child=left_node,
                                            right_child=right_node)
        else:
            return self, left_node, right_node


    def set_target_dir(self, mapping, output_dir):
        """
        :type mapping: dict<path : path>
        ----
        Set Node.target_dir according to selr.orig_file and mapping.
        """
        try:
            self.rel_dir = mapping[dirname(self.orig_file)]
            self.target_dir = opjoin(output_dir, self.rel_dir)
        except KeyError:
            raise KeyError("Cannot find entry for {} in mapping file.".format(
                self.orig_file))


    def build(self):
        """
        Build script in target directory.
        ----
        :type target_dir: path
        """
        makedirs(self.target_dir, exist_ok=True)
        # lines = open(self.orig_file).read().splitlines()
        fout = open(self.target_file, 'a')
        # Write first line according to Node.first_line
        if self.first_line == "SOURCE":
            fout.write("source -echo -verbose {}\n".format(
                self.childs[0][1].rel_file))
        elif self.first_line.startswith("SPLIT"):
            fout.write("##PRS-STAGE-BEGIN: {}\n".format(
                self.first_line.split()[2]))
        elif self.first_line == "ORIG":
            fout.write(linecache.getline(self.orig_file,
                                         self.scope[0]))
        else:
            raise ValueError("Internal error."
                             "Unexpected value of Node.first_line.")
        # Write lines in middle.
        for i in range(self.scope[0]+1, self.scope[1]):
            fout.write(linecache.getline(self.orig_file, i))
        # Write last line according to Node.last_line
        if self.last_line == "SOURCE":
            fout.write("source -echo -verbose {}\n".format(
                self.childs[-1][1].rel_file))
        elif self.last_line.startswith("SPLIT"):
            fout.write("##PRS-STAGE-END: {}\n".format(
                self.last_line.split()[1]))
        elif self.last_line == "ORIG":
            fout.write(linecache.getline(self.orig_file,
                                         self.scope[1]))
        else:
            raise ValueError("Internal error."
                             "Unexpected value of Node.last_line.")
        fout.close()
        linecache.clearcache()


    def __repr__(self):
        return "<Node S: {} D: {}>".format(basename(self.orig_file),
                                           basename(self.target_file))



class Flow(object):
    """
    Data structure of a flow. Consists of a source tree of nodes.
    """

    def __init__(self, source_tree_file, separator_file="", mapping_file=""):
        source_tree = open(source_tree_file)
        top_script = source_tree.readline()[:-1]
        source_tree.close()
        self.top_nodes = [Node(orig_file=top_script)]
        self.top_nodes[0].parse(source_tree_file=source_tree_file)
        self.duplicates = list()
        if separator_file:
            self.separators = self.load_separators(separator_file)
        if mapping_file:
            self.mapping = self.load_mapping(mapping_file)


    def iter_dfs_all(self):
        """
        Loop over all top nodes and apply Node.iter_dfs on each of them.
        """
        for top_node in self.top_nodes:
            for node in top_node.iter_dfs():
                yield node


    def split(self, separator):
        """
        :type separator: Separator
        ----
        Split the source tree according to an input separator. All files on the
        source chain are split.
        """
        # Locate the node to split.
        # If there is only one Node with orig_file==separator.file_name, then the
        # file that contains separator is not split yet. Split this Node.
        # If there are multiple Nodes with orig_file==separator.file_name, then
        # the file that contains separator is already split. Find the last Node
        # with matching stage name, and split this Node.
        if separator.file_name in self.duplicates:
            raise ValueError("Invalid separator location: Separator in {} is"
                             "not supported because this script is sourced more"
                             "than once in the flow")
        matching_nodes = [n for n in self.iter_dfs_all()
                          if n.orig_file == separator.file_name and
                          n.stage in (separator.last_stage, None)]
        node = matching_nodes[-1]
        orig_top, left_top, right_top = node.split_bot_up(
            last_stage=separator.last_stage,
            next_stage=separator.next_stage,
            line_num=separator.line_num-node.scope[0]+1,
            left_child=None,
            right_child=None)
        self.split_top_node(orig_top, left_top, right_top)


    def split_top_node(self, orig_node, left_node, right_node):
        """
        Split a top script node..
        """
        idx_node = self.top_nodes.index(orig_node)
        self.top_nodes[idx_node : (idx_node+1)] = [left_node, right_node]


    def split_all(self):
        """
        Do Flow.split() on all separators in self.separators.
        """
        self.dedup()
        for separator in self.separators:
            self.split(separator)


    def dedup(self):
        """
        :rtype: list(str)
        ----
        Remove duplicated child nodes that points to the same file.
        After dedup a script can only appear once in the source tree.
        Return a list of file names of duplicated scripts.
        """
        all_scripts = list()
        self.duplicates = list()
        for node in self.iter_dfs_all():
            if node.orig_file not in all_scripts:
                all_scripts.append(node.orig_file)
            else:
                idx_child = node.parent.childs.index((node.line_num, node))
                node.parent.childs = node.parent.childs[:idx_child] + \
                        node.parent.childs[idx_child+1:]
                if node.orig_file not in self.duplicates:
                    self.duplicates.append(node.orig_file)
        return self.duplicates


    def set_target_dir_all(self, output_dir):
        """
        :type output_dir: path
        ----
        Iterate over all top nodes and their child nodes, set their target_dir
        according to orig_file, output_dir, and mapping.
        """
        for node in self.iter_dfs_all():
            node.set_target_dir(mapping=self.mapping, output_dir=output_dir)


    def build_all(self, output_dir):
        """
        :type output_dir: path
        """
        if isdir(output_dir):
            raise OSError("Output directory {} already exists.".format(
                output_dir))
        self.set_target_dir_all(output_dir)
        for node in self.iter_dfs_all():
            node.build()


    def move_top_scripts(self, output_dir):
        """
        Move top scripts from unified location (output_dir + mapping) to
        designated location.
        """
        for top_node in self.top_nodes:
            src = top_node.target_file
            dst = opjoin(output_dir, top_node.stage+".tcl")
            print("moving {} to {}.".format(src, dst))
            if not isfile(src):
                raise OSError("File {} does not exist.".format(src))
            if not isdir(output_dir):
                raise OSError("Output directory {} does not exist.".format(
                    output_dir))
            if isfile(dst):
                raise OSError("File {} already exists.".format(dst))
            shutil.move(src, dst)


    def export_all_source_trees(self, unit_indents=2, fout=sys.stdout, verbose=False):
        """
        :type unit_indents: int
        :type fout: file-like object
        :type verbose: bool
        ----
        Show content of all top nodes. In normal mode the output is equivalent
        to input source tree file. In verbose mode the output is appended with
        scope and target file name.
        """
        for top_node in self.top_nodes:
            top_node.export_source_tree(unit_indents=unit_indents,
                                        fout=fout,
                                        verbose=verbose)


    @staticmethod
    def load_separators(separator_file):
        """
        :type separator_file: path
        :rtype separators: list<Separator>
        """
        separator_fid = open(separator_file)
        separators = [Separator(*line.split()) for line in
                      separator_fid.read().splitlines()]
        separator_fid.close()
        return separators


    @staticmethod
    def load_mapping(mapping_file):
        """
        :type mapping_file: path
        :rtype mapping: dict<path : path>
        """
        mapping_fid = open(mapping_file)
        mapping = {t[0] : t[1] for t in
                   [line.split() for line in mapping_fid.read().splitlines()]}
        mapping_fid.close()
        return mapping



class SourceTreeTestCase(unittest.TestCase):
    """
    Unit tests
    """

    def test_parse_source_tree(self):
        """
        Test if Node.parse and Node.export_source_tree works correctly.
        """
        print()
        for i in count(start=1, step=1):
            source_tree_file = 'test/parse_source_tree.{}.txt'.format(i)
            if not isfile(source_tree_file):
                break
            print("Unittest on {} ... ".format(source_tree_file))
            source_tree = open(source_tree_file)
            top_script = source_tree.readline()[:-1]
            source_tree.close()
            node = Node(orig_file=top_script)
            fout = io.StringIO()
            node.parse(source_tree_file)
            node.export_source_tree(fout=fout)
            fin = open(source_tree_file)
            content = fout.getvalue()
            self.assertEqual(content, fin.read())
            fin.close()
            fout.close()
            print('PASS')


    def test_dedup(self):
        """
        Test if Node.dedup works correctly.
        """
        print()
        for i in count(start=1, step=1):
            input_file = 'test/dedup.{}.source_tree.txt'.format(i)
            ref_file = 'test/dedup.{}.ref.txt'.format(i)
            sept_file = 'test/dedup.{}.separators.txt'.format(i)
            dup_file = 'test/dedup.{}.dups.txt'.format(i)
            if not isfile(input_file):
                break
            print('Unittest on {} ... '.format(input_file))
            fin_source_tree = open(ref_file)
            fin_duplicates = open(dup_file)
            fout = io.StringIO()
            flow = Flow(source_tree_file=input_file,
                        separator_file=sept_file)
            duplicates = sorted(flow.dedup())
            flow.top_nodes[0].export_source_tree(fout=fout)
            ref_source_tree = fin_source_tree.read()
            ref_duplicates = sorted(fin_duplicates.read().splitlines())
            self.assertEqual(fout.getvalue(), ref_source_tree)
            self.assertEqual(duplicates, ref_duplicates)
            fin_source_tree.close()
            fin_duplicates.close()
            fout.close()
            print('PASS')


    def test_split(self):
        """
        Test if Flow.split works correctly.
        """
        print()
        for i in count(start=1, step=1):
            input_file = 'test/split.source_tree.txt'
            input_spt_file = 'test/split.{}.separators.txt'.format(i)
            ref_file = 'test/split.{}.ref.txt'.format(i)
            if not isfile(ref_file):
                break
            print('Unittest on {} ... '.format(input_spt_file))
            fout = io.StringIO()
            ref_fid = open(ref_file)
            flow = Flow(source_tree_file=input_file,
                        separator_file=input_spt_file)
            flow.split_all()
            flow.export_all_source_trees(fout=fout)
            content_out = fout.getvalue()
            content_ref = ref_fid.read()
            if content_out != content_ref:
                open("split.{}.out.txt".format(i), 'w').write(content_out)
            self.assertEqual(content_out, content_ref)
            # self.assertEqual(fout.getvalue(), ref_fid.read())
            ref_fid.close()
            print('PASS')


    def test_verbose_split(self):
        """
        Test if Flow.split works correctly.
        """
        print()
        for i in count(start=1, step=1):
            input_file = 'test/split.source_tree.txt'
            input_spt_file = 'test/split.{}.separators.txt'.format(i)
            input_map_file = 'test/split.mapping.txt'
            ref_file = 'test/split.{}.verbose.ref.txt'.format(i)
            if not isfile(ref_file):
                break
            print('Unittest on {} in verbose mode ... '.format(input_spt_file))
            fout = io.StringIO()
            ref_fid = open(ref_file)
            flow = Flow(source_tree_file=input_file,
                        separator_file=input_spt_file,
                        mapping_file=input_map_file)
            flow.split_all()
            flow.set_target_dir_all('')
            flow.export_all_source_trees(fout=fout, verbose=True)
            content_out = fout.getvalue()
            content_ref = ref_fid.read()
            if content_out != content_ref:
                open("split.{}.verbose.out.txt".format(i), 'w').write(
                    content_out)
            self.assertEqual(content_out, content_ref)
            # self.assertEqual(fout.getvalue(), ref_fid.read())
            ref_fid.close()
            print('PASS')


def manual_test_build(output_dir="export"):
    """
    Test if Flow.build works correctly.
    """
    if isdir(output_dir):
        shutil.rmtree(output_dir)
    input_tree_file = 'test/split.source_tree.txt'
    input_spt_file = 'test/split.5.separators.txt'
    input_map_file = 'test/split.mapping.txt'
    flow = Flow(source_tree_file=input_tree_file,
                separator_file=input_spt_file,
                mapping_file=input_map_file)
    flow.split_all()
    flow.build_all(output_dir)
    print("build completed.")
    flow.move_top_scripts(output_dir)


if __name__ == "__main__":
    # unittest.main()
    manual_test_build()
