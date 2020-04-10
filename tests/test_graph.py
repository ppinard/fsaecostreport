""""""

# Standard library modules.
import unittest
import logging
import os

# Third party modules.

# Local modules.
from fsaecostreport.reader import SystemFileReader, MetadataReader
import fsaecostreport.graph as graph

# Globals and constants variables.


class Test(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.basepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "testdata"
        )

        self.metadata = MetadataReader().read(self.basepath)

        for system in self.metadata.systems:
            SystemFileReader().read(self.basepath, system)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testgraph_costsummary(self):
        graph.cost_summary(self.basepath, self.metadata)

        path = os.path.join(self.basepath, "cost_summary.pdf")
        self.assertTrue(os.path.exists(path))
        os.remove(path)


if __name__ == "__main__":  # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
