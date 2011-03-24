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
import os.path

# Third party modules.

# Local modules.
from fsaecostreport.writer import eBOMWriter, CostReportLaTeXWriter

from fsaecostreport.system import System
from fsaecostreport.reader import SystemFileReader, MetadataReader

# Globals and constants variables.
TM = System("TM", "Random stuff", "Z", (255, 0, 0))

class TesteBOMWriter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        TM.clear_components()

        basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        self.system = SystemFileReader().read(basepath, TM)
        self.metadata = MetadataReader().read(basepath)

        self.writer = eBOMWriter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testwrite(self):
        rows = self.writer._create_rows([self.system], self.metadata, {})
        self.assertEqual(12, len(rows))

class TestCostReportLaTeXWriter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        TM.clear_components()

        self.basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        self.system = SystemFileReader().read(self.basepath, TM)
        self.metadata = MetadataReader().read(self.basepath)

        self.writer = CostReportLaTeXWriter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testwrite(self):
        lines = self.writer._write(self.basepath, [self.system], self.metadata)
        self.assertEqual(286, len(lines))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
