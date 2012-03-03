"""
================================================================================
:mod:`test_component` -- Unit tests for the module :mod:`component`.
================================================================================

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from fsaecostreport.component import _Component

# Globals and constants variables.

class ComponentMock(_Component):
    def __init__(self, system_label, pn_base, revision):
        _Component.__init__(self, "", system_label, "mock", pn_base, revision)

class Test_Component(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test__cmp__(self):
        # system label
        c1 = ComponentMock("TM", "A1000", "AA")
        c2 = ComponentMock("BR", "A1000", "AA")
        c3 = ComponentMock("WT", "A1000", "AA")

        cs = sorted([c1, c2, c3]) # c3, c1, c2
        self.assertEqual(c3, cs[0])
        self.assertEqual(c1, cs[1])
        self.assertEqual(c2, cs[2])

        # assembly or part number
        c4 = ComponentMock("TM", "A1000", "AA")
        c5 = ComponentMock("TM", "00100", "AA")

        cs = sorted([c4, c5]) # c5, c4
        self.assertEqual(c5, cs[0])
        self.assertEqual(c4, cs[1])

        # designation
        c6 = ComponentMock("TM", "A1000", "AA")
        c7 = ComponentMock("TM", "A0000", "AA")
        c8 = ComponentMock("TM", "A2000", "AA")

        cs = sorted([c6, c7, c8]) # c7, c6, c8
        self.assertEqual(c7, cs[0])
        self.assertEqual(c6, cs[1])
        self.assertEqual(c8, cs[2])

        # category
        c9 = ComponentMock("TM", "00100", "AA")
        c10 = ComponentMock("TM", "00000", "AA")
        c11 = ComponentMock("TM", "00300", "AA")

        cs = sorted([c9, c10, c11]) # c10, c11, c9
        self.assertEqual(c10, cs[0])
        self.assertEqual(c11, cs[1])
        self.assertEqual(c9, cs[2])

        # counter
        c12 = ComponentMock("TM", "00115", "AA")
        c13 = ComponentMock("TM", "00102", "AA")
        c14 = ComponentMock("TM", "00199", "AA")

        cs = sorted([c12, c13, c14]) # c13, c12, c14
        self.assertEqual(c13, cs[0])
        self.assertEqual(c12, cs[1])
        self.assertEqual(c14, cs[2])

        # revision
        c15 = ComponentMock("TM", "00115", "AA")
        c16 = ComponentMock("TM", "00115", "BB")
        c17 = ComponentMock("TM", "00115", "AB")

        cs = sorted([c15, c16, c17]) # c15, c17, c16
        self.assertEqual(c15, cs[0])
        self.assertEqual(c17, cs[1])
        self.assertEqual(c16, cs[2])

        ### Overall
        cs = sorted(set([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12,
                         c13, c14, c15, c16, c17]),
                    reverse=True)


if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
