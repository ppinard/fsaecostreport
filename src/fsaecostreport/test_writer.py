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
from fsaecostreport.writer import eBOMWriter, CostReportLaTeXWriter, FSGBOMWriter
from fsaecostreport.reader import SystemFileReader, MetadataReader

# Globals and constants variables.

class TesteBOMWriter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')

        self.metadata = MetadataReader().read(basepath)

        for system in self.metadata.systems:
            SystemFileReader().read(basepath, system)

        self.writer = eBOMWriter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testwrite(self):
        rows = self.writer._create_rows(self.metadata, {})
        self.assertEqual(15, len(rows))

class TestCostReportLaTeXWriter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')

        self.metadata = MetadataReader().read(self.basepath)

        for system in self.metadata.systems:
            SystemFileReader().read(self.basepath, system)

        self.writer = CostReportLaTeXWriter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testwrite(self):
        lines = self.writer._write(self.basepath, self.metadata)
        self.assertEqual(443, len(lines))

#        self.writer.write(self.basepath, self.metadata)

class TestFSGBOMWriter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')

        self.metadata = MetadataReader().read(self.basepath)

        for system in self.metadata.systems:
            SystemFileReader().read(self.basepath, system)

        self.writer = FSGBOMWriter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testwrite(self):
        self.writer.write(self.basepath, self.metadata)
        os.remove(os.path.join(self.basepath, 'costreport.xlsx'))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
