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

import unittest
from itertools import count

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
        self.target_dir = ""


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
            target_file = opjoin(target_dir, basename(target_file))
        return target_file


    # def add_child(self, orig_file, start=0, end=0, line_num=0):
    #     """
    #     Create child script node and link to parent node.
    #     """
    #     child = Node(orig_file=orig_file, parent=self, line_num=line_num)
    #     child.scope = [start, end]
    #     self.childs.append((line_num, child))
    #     print("added child {} to {}".format(child, self))
    #     return child


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


    def export_source_tree(self, unit_indents=2, fout=sys.stdout):
        """
        Show content of a node.
        """
        stack = [(-1, 0, self), ]
        fout.write("{}\n".format(self.target_file))
        while stack:
            indents, line_num, node = stack.pop()
            stack.extend([(indents + 1, t[0], t[1])
                          for t in reversed(node.childs)])
            if indents == -1:
                continue
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
        left_node.scope = [self.scope[0], line_num]
        left_node.childs = [t for t in self.childs if t[0] < line_num]
        for _, child_node in left_node.childs:
            child_node.parent = left_node
        if left_child:
            left_node.add_child_node(left_child, line_num-self.scope[0]+1)
        # Implement right node, link right node and right child node.
        right_node = Node(orig_file=self.orig_file)
        right_node.stage = next_stage
        right_node.scope = [line_num, self.scope[1]]
        right_node.childs = [(t[0] - (line_num - 1), t[1]) for t in self.childs
                             if t[0] > line_num]
        for _, child_node in right_node.childs:
            child_node.parent = right_node
            child_node.line_num -= (line_num - 1)
        if right_child:
            right_node.add_child_node(right_child, 1, prepend=True)
        # Recursively split parent node unless current node is the top one.
        if self.parent:
            return self.parent.split_bot_up(last_stage=last_stage,
                                            next_stage=next_stage,
                                            line_num=self.line_num,
                                            left_child=left_node,
                                            right_child=right_node)
        else:
            return self, left_node, right_node


    # def split(self, last_stage, next_stage, line_num,
    #           left_child, right_child):
    #     """
    #     :type last_stage: string
    #     :type next_stage: string
    #     :type line_num: int
    #     :type left_child: Node
    #     :type right_child: Node
    #     :rtype left_node: Node
    #     :rtype right_node: Node
    #     ----
    #     Split node according to an input separator plus the split nodes from
    #     lower layer. Return the two new nodes after splitting.
    #     """
    #     # Implement left node, link left node and left child node.
    #     left_node = Node(orig_file=self.orig_file)
    #     left_node.stage = last_stage
    #     left_node.scope = [self.scope[0], line_num]
    #     left_node.childs = [t for t in self.childs if t[0] < line_num]
    #     for _, child_node in left_node.childs:
    #         child_node.parent = left_node
    #     if left_child:
    #         left_node.add_child_node(left_child)
    #     # Implement right node, link right node and right child node.
    #     right_node = Node(orig_file=self.orig_file)
    #     right_node.stage = next_stage
    #     right_node.scope = [line_num, self.scope[1]]
    #     right_node.childs = [(t[0] - line_num + 1, t[1]) for t in self.childs
    #                          if t[0] > line_num]
    #     for _, child_node in right_node.childs:
    #         child_node.parent = right_node
    #         child_node.line_num -= (line_num - 1)
    #     if right_child:
    #         right_node.add_child_node(right_child)
    #     # Return left child and right child
    #     return left_node, right_node


    def build(self, target_dir, is_top=False):
        """
        Build script in target directory.
        ----
        :type target_dir: path
        """
        makedirs(target_dir, exist_ok=True)
        lines = open(self.orig_file).read().splitlines()
        if is_top:
            print("Export top node {}.".format(self))
            target_file = opjoin(target_dir, '{}.tcl'.format(self.stage))
        else:
            target_file = opjoin(target_dir, basename(self.target_file))
        fout = open(target_file, 'a')
        fout.write('\n'.join(lines[self.scope[0]-1 : self.scope[1]-1]))
        fout.close()


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


    def iter_dfs(self):
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
        matching_nodes = [n for n in self.iter_dfs()
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
        for node in self.iter_dfs():
            if node.orig_file not in all_scripts:
                all_scripts.append(node.orig_file)
            else:
                idx_child = node.parent.childs.index((node.line_num, node))
                node.parent.childs = node.parent.childs[:idx_child] + \
                        node.parent.childs[idx_child+1:]
                if node.orig_file not in self.duplicates:
                    self.duplicates.append(node.orig_file)
        return self.duplicates


    def build(self, output_dir):
        """
        :type output_dir: path
        """
        self.dedup()
        for separator in self.separators:
            self.split(separator)
        # if isdir(output_dir):
        #     raise OSError("Output directory {} already exists.".format(
        #         output_dir))
        # for node in self.iter_dfs():
        #     if node.orig_file == "__VIRTUAL_TOP__":
        #         continue
        #     elif node.orig_file == self.root.childs[0][1].orig_file:
        #         target_dir = opjoin(output_dir, 'CONSTRAINT')
        #         is_top = True
        #     else:
        #         target_dir = opjoin(output_dir,
        #                             self.mapping[dirname(node.orig_file)])
        #         is_top = False
        #     node.build(target_dir=target_dir, is_top=is_top)


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
        Test if Node.split works correctly.
        """
        print()
        for i in count(start=1, step=1):
            input_file = 'test/split.{}.source_tree.txt'.format(i)
            input_spt_file = 'test/split.{}.separators.txt'.format(i)
            ref_file = 'test/split.{}.ref.txt'.format(i)
            if not isfile(input_file):
                break
            print('Unittest on {} ... '.format(input_file))
            fout = io.StringIO()
            ref_fid = open(ref_file)
            flow = Flow(source_tree_file=input_file,
                        separator_file=input_spt_file)
            flow.split_all()
            for top_node in flow.top_nodes:
                top_node.export_source_tree(fout=fout)
            content_out = fout.getvalue()
            content_ref = ref_fid.read()
            if content_out != content_ref:
                open("split.{}.out.txt".format(i), 'w').write(content_out)
            self.assertEqual(content_out, content_ref)
            # self.assertEqual(fout.getvalue(), ref_fid.read())
            ref_fid.close()
            print('PASS')


if __name__ == "__main__":
    unittest.main()
