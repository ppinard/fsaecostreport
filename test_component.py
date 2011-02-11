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

        self.assertTrue(c2 > c1)
        self.assertTrue(c2 > c3)
        self.assertTrue(c2 > c3)

        # assembly or part number
        c1 = ComponentMock("TM", "A1000", "AA")
        c2 = ComponentMock("TM", "01000", "AA")
        self.assertTrue(c1 > c2)

        # designation
        c1 = ComponentMock("TM", "A1000", "AA")
        c2 = ComponentMock("TM", "A0000", "AA")
        c3 = ComponentMock("TM", "A2000", "AA")
        self.assertTrue(c1 > c2)
        self.assertTrue(c3 > c1)
        self.assertTrue(c3 > c2)
        self.assertTrue(c2 < c1)
        self.assertTrue(c1 < c3)
        self.assertTrue(c2 < c3)

        # category
        c1 = ComponentMock("TM", "00100", "AA")
        c2 = ComponentMock("TM", "00000", "AA")
        c3 = ComponentMock("TM", "00300", "AA")
        self.assertTrue(c1 > c2)
        self.assertTrue(c3 > c1)
        self.assertTrue(c3 > c2)

        # counter
        c1 = ComponentMock("TM", "001015", "AA")
        c2 = ComponentMock("TM", "001002", "AA")
        c3 = ComponentMock("TM", "001099", "AA")
        self.assertTrue(c1 > c2)
        self.assertTrue(c3 > c1)
        self.assertTrue(c3 > c2)

        # revision
        c1 = ComponentMock("TM", "001015", "AA")
        c2 = ComponentMock("TM", "001015", "BB")
        c3 = ComponentMock("TM", "001015", "AB")
        self.assertTrue(c2 > c1)
        self.assertTrue(c3 > c1)
        self.assertTrue(c2 > c3)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
