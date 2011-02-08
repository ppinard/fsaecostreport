"""
================================================================================
:mod:`test_writer` -- Unit tests for the module MODULE.
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
import os

# Third party modules.

# Local modules.
from writer import CostReportLaTeXWriter
from reader import SystemFileReader, read_year, read_introduction
from system import System

# Globals and constants variables.
TM = System("TM", "Random stuff", "Z", (255, 0, 0))

class Test_ComponentLaTeXWriter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        TM.clear_components()

        self.testdata = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        SystemFileReader().read(self.testdata, TM)

        year = read_year(self.testdata)
        introduction = read_introduction(self.testdata)

        self.writer = CostReportLaTeXWriter([TM], year, introduction)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testwrite_materials(self):
        self.writer.write(self.testdata)


if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
