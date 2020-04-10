"""
================================================================================
:mod:`test_system` -- Unit tests for the module :mod:`system`.
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
from fsaecostreport.system import System
from fsaecostreport.reader import SystemFileReader

# Globals and constants variables.
TM = System(1, "TM", "Random stuff", (255, 0, 0))


class TestSystem(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        TM.clear_components()

        basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        self.system = SystemFileReader().read(basepath, TM)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testhierarchy(self):
        assy1 = self.system.get_component("TM-A1000-AA")
        assy2 = self.system.get_component("TM-A0001-AA")
        assy3 = self.system.get_component("TM-A0002-AA")
        part = self.system.get_component("TM-00001-AA")

        expected = [assy1, assy2, part, assy3]
        actual = self.system.get_hierarchy()
        self.assertEqual(expected, actual)


if __name__ == "__main__":  # pragma: no cover
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
