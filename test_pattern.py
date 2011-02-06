"""
================================================================================
:mod:`test_pattern` -- Unit tests for the module MODULE.
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
from pattern import SYS_ASSY_PN, SUB_ASSY_PN, PART_PN

# Globals and constants variables.

class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.sys_assy = 'TM-A1000-AA'
        self.sub_assy = 'TM-A0101-AA'
        self.part = 'TM-00102-BB'

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testsys_assy_pn(self):
        self.assertTrue(SYS_ASSY_PN.match(self.sys_assy))
        self.assertFalse(SUB_ASSY_PN.match(self.sys_assy))
        self.assertFalse(PART_PN.match(self.sys_assy))

    def testsub_assy_pn(self):
        self.assertFalse(SYS_ASSY_PN.match(self.sub_assy))
        self.assertTrue(SUB_ASSY_PN.match(self.sub_assy))
        self.assertFalse(PART_PN.match(self.sub_assy))

    def testpart_pn(self):
        self.assertFalse(SYS_ASSY_PN.match(self.part))
        self.assertFalse(SUB_ASSY_PN.match(self.part))
        self.assertTrue(PART_PN.match(self.part))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
