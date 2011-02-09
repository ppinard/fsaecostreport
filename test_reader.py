"""
================================================================================
:mod:`test_reader` -- Unit tests for the module MODULE.
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
from system import System
from reader import \
    PartFileReader, AssemblyFileReader, SystemFileReader, MetadataReader

# Globals and constants variables.
TM = System("TM", "Random stuff", "Z", (255, 0, 0))

class TestPartReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        TM.clear_components()

        testdata = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        filepath = os.path.join(testdata, 'TM', 'components', 'TM-00001-AA.csv')
        self.part = PartFileReader().read(filepath, TM)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testheader(self):
        self.assertEqual('Cup holder', self.part.name)
        self.assertEqual('00001', self.part.pn_base)
        self.assertEqual('AA', self.part.revision)
        self.assertEqual('', self.part.details)
        self.assertEqual('TM-00001-AA', self.part.partnumber)
        self.assertEqual('TM-00001-AA', self.part.pn)
        self.assertEqual(0, self.part.quantity)

    def testmaterials(self):
        self.assertEqual(2, len(self.part.materials))

        material = self.part.materials[0]
        self.assertEqual(754, material.id)
        self.assertEqual('Titanium (per kg)', material.name)
        self.assertEqual('ring', material.use)
        self.assertAlmostEqual(8.8, material.unitcost)
        self.assertAlmostEqual(0.4, material.size1)
        self.assertEqual('kg', material.unit1)
        self.assertEqual(None, material.size2)
        self.assertEqual(None, material.unit2)
        self.assertAlmostEqual(1, material.quantity)
        self.assertAlmostEqual(8.8, material.subtotal)

        material = self.part.materials[1]
        self.assertEqual(754, material.id)
        self.assertEqual('Titanium (per kg)', material.name)
        self.assertEqual('bottom', material.use)
        self.assertAlmostEqual(4.4, material.unitcost)
        self.assertAlmostEqual(0.2, material.size1)
        self.assertEqual('kg', material.unit1)
        self.assertEqual(None, material.size2)
        self.assertEqual(None, material.unit2)
        self.assertAlmostEqual(1, material.quantity)
        self.assertAlmostEqual(4.4, material.subtotal)

    def testprocesses(self):
        self.assertEqual(2, len(self.part.processes))

        process = self.part.processes[0]
        self.assertEqual(141, process.id)
        self.assertEqual('Sheet metal bends', process.name)
        self.assertEqual('bend bottom', process.use)
        self.assertAlmostEqual(0.25, process.unitcost)
        self.assertEqual('bend', process.unit)
        self.assertAlmostEqual(1, process.quantity)
        self.assertEqual(None, process.multiplier_id)
        self.assertEqual(None, process.multiplier)
        self.assertAlmostEqual(0.25, process.subtotal)

        process = self.part.processes[1]
        self.assertEqual(136, process.id)
        self.assertEqual('Tapping holes', process.name)
        self.assertEqual('drill holes', process.use)
        self.assertAlmostEqual(0.35, process.unitcost)
        self.assertEqual('hole', process.unit)
        self.assertAlmostEqual(4, process.quantity)
        self.assertEqual(20, process.multiplier_id)
        self.assertEqual(3.65, process.multiplier)
        self.assertAlmostEqual(5.11, process.subtotal)

    def testfasteners(self):
        self.assertEqual(2, len(self.part.fasteners))

        fastener = self.part.fasteners[0]
        self.assertEqual(30, fastener.id)
        self.assertEqual('Nut, Grade 10.9 (SAE 8)', fastener.name)
        self.assertEqual('Attach bottom to ring', fastener.use)
        self.assertAlmostEqual(0.05, fastener.unitcost)
        self.assertAlmostEqual(25.4, fastener.size1)
        self.assertEqual('mm', fastener.unit1)
        self.assertEqual(5.4, fastener.size2)
        self.assertEqual('mm', fastener.unit2)
        self.assertAlmostEqual(4, fastener.quantity)
        self.assertAlmostEqual(0.2, fastener.subtotal)

        fastener = self.part.fasteners[1]
        self.assertEqual(17, fastener.id)
        self.assertEqual('Bolt, Grade 10.9 (SAE 8)', fastener.name)
        self.assertEqual('Attach bottom to ring', fastener.use)
        self.assertAlmostEqual(0.1, fastener.unitcost)
        self.assertAlmostEqual(25.4, fastener.size1)
        self.assertEqual('mm', fastener.unit1)
        self.assertEqual(5.4, fastener.size2)
        self.assertEqual('mm', fastener.unit2)
        self.assertAlmostEqual(4, fastener.quantity)
        self.assertAlmostEqual(0.4, fastener.subtotal)

    def testtoolings(self):
        self.assertEqual(1, len(self.part.toolings))

        tooling = self.part.toolings[0]
        self.assertEqual(11, tooling.id)
        self.assertEqual('Welds - Welding Fixture', tooling.name)
        self.assertEqual('', tooling.use)
        self.assertAlmostEqual(500, tooling.unitcost)
        self.assertEqual('point', tooling.unit)
        self.assertAlmostEqual(5, tooling.quantity)
        self.assertAlmostEqual(3000, tooling.pvf)
        self.assertAlmostEqual(0.8333333, tooling.subtotal)

    def testdrawings(self):
        self.assertEqual(1, len(self.part.drawings))
        self.assertEqual('TM-00001-AA.pdf', os.path.basename(self.part.drawings[0]))

    def testpictures(self):
        self.assertEqual(0, len(self.part.pictures))

class TestAssemblyReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        TM.clear_components()

        testdata = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        filepath = os.path.join(testdata, 'TM', 'components', 'TM-A0001-AA.csv')
        self.assy = AssemblyFileReader().read(filepath, TM)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testheader(self):
        self.assertEqual('Push bar', self.assy.name)
        self.assertEqual('A0001', self.assy.pn_base)
        self.assertEqual('AA', self.assy.revision)
        self.assertEqual('', self.assy.details)
        self.assertEqual('TM-A0001-AA', self.assy.partnumber)
        self.assertEqual('TM-A0001-AA', self.assy.pn)
        self.assertEqual(2, self.assy.quantity)

    def testcomponents(self):
        self.assertEqual(1, len(self.assy.components))

        component = self.assy.components.keys()[0]
        self.assertEqual('Cup holder', component.name)
        self.assertEqual('00001', component.pn_base)
        self.assertEqual('AA', component.revision)
        self.assertEqual('', component.details)
        self.assertEqual('TM-00001-AA', component.partnumber)
        self.assertEqual('TM-00001-AA', component.pn)

        quantity = self.assy.components.values()[0]
        self.assertEqual(2, quantity)

    def testmaterials(self):
        self.assertEqual(2, len(self.assy.materials))

        material = self.assy.materials[0]
        self.assertEqual(752, material.id)
        self.assertEqual('Steel, Mild (per kg)', material.name)
        self.assertEqual('Tube', material.use)
        self.assertAlmostEqual(1.125, material.unitcost)
        self.assertAlmostEqual(0.5, material.size1)
        self.assertEqual('kg', material.unit1)
        self.assertEqual(None, material.size2)
        self.assertEqual(None, material.unit2)
        self.assertAlmostEqual(1, material.quantity)
        self.assertAlmostEqual(1.125, material.subtotal)

        material = self.assy.materials[1]
        self.assertEqual(752, material.id)
        self.assertEqual('Steel, Mild (per kg)', material.name)
        self.assertEqual('Handle', material.use)
        self.assertAlmostEqual(0.9, material.unitcost)
        self.assertAlmostEqual(0.4, material.size1)
        self.assertEqual('kg', material.unit1)
        self.assertEqual(None, material.size2)
        self.assertEqual(None, material.unit2)
        self.assertAlmostEqual(1, material.quantity)
        self.assertAlmostEqual(0.9, material.subtotal)

    def testprocesses(self):
        self.assertEqual(2, len(self.assy.processes))

        process = self.assy.processes[0]
        self.assertEqual(150, process.id)
        self.assertEqual('Weld - Round Tubing', process.name)
        self.assertEqual('Weld handle to main tube', process.use)
        self.assertAlmostEqual(0.38, process.unitcost)
        self.assertEqual('cm', process.unit)
        self.assertAlmostEqual(5, process.quantity)
        self.assertEqual(None, process.multiplier_id)
        self.assertEqual(None, process.multiplier)
        self.assertAlmostEqual(1.9, process.subtotal)

        process = self.assy.processes[1]
        self.assertEqual(150, process.id)
        self.assertEqual('Weld - Round Tubing', process.name)
        self.assertEqual('Weld cup holder to tube', process.use)
        self.assertAlmostEqual(0.38, process.unitcost)
        self.assertEqual('cm', process.unit)
        self.assertAlmostEqual(4, process.quantity)
        self.assertEqual(22, process.multiplier_id)
        self.assertEqual(2, process.multiplier)
        self.assertAlmostEqual(3.04, process.subtotal)

    def testfasteners(self):
        self.assertEqual(0, len(self.assy.fasteners))

    def testtoolings(self):
        self.assertEqual(1, len(self.assy.toolings))

        tooling = self.assy.toolings[0]
        self.assertEqual(11, tooling.id)
        self.assertEqual('Welds - Welding Fixture', tooling.name)
        self.assertEqual('Weld', tooling.use)
        self.assertAlmostEqual(500, tooling.unitcost)
        self.assertEqual('point', tooling.unit)
        self.assertAlmostEqual(5, tooling.quantity)
        self.assertAlmostEqual(3000, tooling.pvf)
        self.assertAlmostEqual(0.8333333, tooling.subtotal)

    def testdrawings(self):
        self.assertEqual(0, len(self.assy.drawings))

    def testpictures(self):
        self.assertEqual(1, len(self.assy.pictures))
        self.assertEqual('TM-A0001-AA.jpg', os.path.basename(self.assy.pictures[0]))

class TestSystemReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        self.system = SystemFileReader().read(basepath, TM)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertTrue(True)

    def testcomponents(self):
        self.assertEqual(4, len(self.system._components))

        assy1 = self.system.get_component('TM-A1000-AA')
        assy2 = self.system.get_component('TM-A0001-AA')
        assy3 = self.system.get_component('TM-A0002-AA')
        part = self.system.get_component('TM-00001-AA')

        self.assertEqual('Pusher', assy1.name)
        self.assertEqual('A1000', assy1.pn_base)
        self.assertEqual('AA', assy1.revision)
        self.assertEqual('', assy1.details)
        self.assertEqual('TM-A1000-AA', assy1.partnumber)
        self.assertEqual('TM-A1000-AA', assy1.pn)
        self.assertEqual(1, len(assy1.components))
        self.assertEqual(assy2, assy1.components.keys()[0])
        self.assertEqual(2, assy1.components.values()[0])
        self.assertEqual(1, assy1.quantity)
        self.assertEqual(0, len(assy1.parents))
        self.assertEqual(1, assy1.quantity)

        self.assertEqual('Push bar', assy2.name)
        self.assertEqual('A0001', assy2.pn_base)
        self.assertEqual('AA', assy2.revision)
        self.assertEqual('', assy2.details)
        self.assertEqual('TM-A0001-AA', assy2.partnumber)
        self.assertEqual('TM-A0001-AA', assy2.pn)
        self.assertEqual(1, len(assy2.components))
        self.assertEqual(part, assy2.components.keys()[0])
        self.assertEqual(2, assy2.components.values()[0])
        self.assertEqual(1, len(assy2.parents))
        self.assertEqual(assy1, list(assy2.parents)[0])
        self.assertEqual(2, assy2.quantity)

        self.assertEqual('Cart', assy3.name)
        self.assertEqual('A0002', assy3.pn_base)
        self.assertEqual('AA', assy3.revision)
        self.assertEqual('', assy3.details)
        self.assertEqual('TM-A0002-AA', assy3.partnumber)
        self.assertEqual('TM-A0002-AA', assy3.pn)
        self.assertEqual(1, len(assy3.components))
        self.assertEqual(part, assy3.components.keys()[0])
        self.assertEqual(3, assy3.components.values()[0])
        self.assertEqual(1, assy3.quantity)
        self.assertEqual(0, len(assy3.parents))
        self.assertEqual(1, assy3.quantity)

        self.assertEqual('Cup holder', part.name)
        self.assertEqual('00001', part.pn_base)
        self.assertEqual('AA', part.revision)
        self.assertEqual('', part.details)
        self.assertEqual('TM-00001-AA', part.partnumber)
        self.assertEqual('TM-00001-AA', part.pn)
        self.assertEqual(2, len(part.parents))
        self.assertTrue(assy2 in part.parents)
        self.assertTrue(assy3 in part.parents)
        self.assertEqual(7, part.quantity)

class TestMetadataReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        self.metadata = MetadataReader().read(basepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(2011, self.metadata.year)
        self.assertEqual(49, self.metadata.car_number)
        self.assertEqual('McGill University', self.metadata.university)
        self.assertEqual('McGill Racing Team', self.metadata.team_name)
        self.assertEqual(['Intro', 'BLAH'], self.metadata.introduction)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
