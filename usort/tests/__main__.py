# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import unittest

from .functional import BasicOrderingTest, UsortStringFunctionalTest  # noqa: F401
from .sort_key import SortableImportTest  # noqa: F401

unittest.main()