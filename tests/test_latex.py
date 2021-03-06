""""""

# Standard library modules.
import unittest
import logging
import os.path

# Third party modules.

# Local modules.
from fsaecostreport.latex import AuxReader

# Globals and constants variables.


class TestAuxReader(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.basepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "testdata"
        )
        self.reader = AuxReader()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testread(self):
        pagerefs = self.reader.read(self.basepath)

        self.assertEqual(3, pagerefs["TM-A1000-AA"])
        self.assertEqual(4, pagerefs["TM-A0001-AA"])
        self.assertEqual(6, pagerefs["TM-A0002-AA"])
        self.assertEqual(5, pagerefs["TM-00001-AA"])


if __name__ == "__main__":  # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
