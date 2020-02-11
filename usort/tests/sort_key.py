# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest

import libcst as cst

from ..sorting import Config, SortableImport


class SortableImportTest(unittest.TestCase):
    def test_from_node_Import(self) -> None:
        imp = SortableImport.from_node(cst.parse_statement("import a"), Config())
        self.assertEqual("a", imp.first_module)
        self.assertEqual("a", imp.first_dotted_import)
        self.assertEqual({"a"}, imp.imported_names)

        imp = SortableImport.from_node(cst.parse_statement("import a, b"), Config())
        self.assertEqual("a", imp.first_module)
        self.assertEqual("a", imp.first_dotted_import)
        self.assertEqual({"a", "b"}, imp.imported_names)

        imp = SortableImport.from_node(cst.parse_statement("import a as b"), Config())
        self.assertEqual("a", imp.first_module)
        self.assertEqual("a", imp.first_dotted_import)
        self.assertEqual({"b"}, imp.imported_names)

        imp = SortableImport.from_node(cst.parse_statement("import os.path"), Config())
        self.assertEqual("os.path", imp.first_module)
        self.assertEqual("os.path", imp.first_dotted_import)
        self.assertEqual({"os"}, imp.imported_names)

    def test_from_node_ImportFrom(self) -> None:
        imp = SortableImport.from_node(cst.parse_statement("from a import b"), Config())
        self.assertEqual("a", imp.first_module)
        self.assertEqual("b", imp.first_dotted_import)
        self.assertEqual({"b"}, imp.imported_names)

        imp = SortableImport.from_node(
            cst.parse_statement("from a import b as c"), Config()
        )
        self.assertEqual("a", imp.first_module)
        self.assertEqual("b", imp.first_dotted_import)
        self.assertEqual({"c"}, imp.imported_names)

    def test_from_node_ImportFrom_relative(self) -> None:
        imp = SortableImport.from_node(
            cst.parse_statement("from .a import b"), Config()
        )
        self.assertEqual(".a", imp.first_module)
        self.assertEqual("a", imp.first_dotted_import)
        self.assertEqual({"b"}, imp.imported_names)

        imp = SortableImport.from_node(
            cst.parse_statement("from ...a import b"), Config()
        )
        self.assertEqual("...a", imp.first_module)
        self.assertEqual("a", imp.first_dotted_import)
        self.assertEqual({"b"}, imp.imported_names)

        imp = SortableImport.from_node(cst.parse_statement("from . import a"), Config())
        self.assertEqual(".", imp.first_module)
        self.assertEqual("a", imp.first_dotted_import)
        self.assertEqual({"a"}, imp.imported_names)

        imp = SortableImport.from_node(
            cst.parse_statement("from .. import a"), Config()
        )
        self.assertEqual("..", imp.first_module)
        self.assertEqual("a", imp.first_dotted_import)
        self.assertEqual({"a"}, imp.imported_names)

        imp = SortableImport.from_node(
            cst.parse_statement("from . import a as b"), Config()
        )
        self.assertEqual(".", imp.first_module)
        self.assertEqual("a", imp.first_dotted_import)
        self.assertEqual({"b"}, imp.imported_names)