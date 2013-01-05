"""
================================================================================
:mod:`test_graph` -- Unit tests for the module MODULE.
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
from fsaecostreport.system import System
from fsaecostreport.reader import SystemFileReader, MetadataReader

import fsaecostreport.graph as graph

# Globals and constants variables.
TM = System("TM", "Random stuff", "Y", (255, 0, 0))
FI = System("FI", "Finance stuff", "Z", (0, 255, 0))

class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        TM.clear_components()
        FI.clear_components()

        self.basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        self.system1 = SystemFileReader().read(self.basepath, TM)
        self.system2 = SystemFileReader().read(self.basepath, FI)
        self.metadata = MetadataReader().read(self.basepath)
        self.metadata.systems = [self.system1, self.system2]

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testgraph_costsummary(self):
        graph.cost_summary(self.basepath, self.metadata)

        path = os.path.join(self.basepath, 'cost_summary.pdf')
        self.assertTrue(os.path.exists(path))
        os.remove(path)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
