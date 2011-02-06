#!/usr/bin/env python
"""
================================================================================
:mod:`reader` -- 
================================================================================

.. module:: reader
   :synopsis: 

.. inheritance-diagram:: reader

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import csv
import operator
import os.path
import logging
import glob

# Third party modules.

# Local modules.
from costtable import Material, Process, Fastener, Tooling
from system import Part, Assembly
from pattern import SYS_ASSY_PN, SUB_ASSY_PN, PART_PN

# Globals and constants variables.
COMPONENTS_DIR = "components"
DRAWINGS_DIR = "drawings"
PICTURES_DIR = "pictures"

class _ComponentReader(object):
    def _get_lines(self, filepath):
        logging.debug("Reading csv")
        reader = csv.reader(open(filepath, 'r'))
        logging.debug("Reading csv... DONE")
        return list(reader)

    def _find_line(self, lookup, lines):
        firstcol_getter = operator.itemgetter(0)
        firstcol = map(firstcol_getter, lines)

        return firstcol.index(lookup)

    def _assert_equal(self, a, b, context="", places=4):
        if round(abs(b - a), places) != 0:
            raise AssertionError, context + ": %s != %s" % (a, b)

    def _check_filename(self, filepath, pn):
        filename = os.path.splitext(os.path.basename(filepath))[0]
        if filename != pn:
            raise AssertionError, \
                "filename (%s) != part number (%s)" % (filename, pn)

    def _read_materials(self, lines):
        logging.debug("Reading materials ...")

        firstline_index = self._find_line('Materials', lines) + 2
        materials = []

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            materials.append(self._read_material(line))

        logging.debug("Reading materials ... DONE")
        return materials

    def _read_material(self, line):
        id = int(line[0])
        name = line[1].strip()
        use = line[2].strip()
        unitcost = float(line[3])

        if line[5].strip():
            size1 = float(line[4])
            unit1 = line[5].strip()
        else:
            size1 = unit1 = None

        if line[7].strip():
            size2 = float(line[6])
            unit2 = line[7].strip()
        else:
            size2 = unit2 = None

        quantity = float(line[8])

        material = Material(id, name, use, unitcost, size1, unit1, size2, unit2, quantity)

        # check
        self._assert_equal(material.subtotal, float(line[9]), "material subtotal")

        return material

    def _read_processes(self, lines):
        logging.debug("Reading processes ...")

        firstline_index = self._find_line('Processes', lines) + 2
        processes = []

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            processes.append(self._read_process(line))

        logging.debug("Reading processes ... DONE")
        return processes

    def _read_process(self, line):
        id = int(line[0])
        name = line[1].strip()
        use = line[2].strip()
        unitcost = float(line[3])
        unit = line[4].strip()
        quantity = float(line[5])

        if line[6].strip():
            multiplier_id = int(line[6])
            multiplier = float(line[7])
        else:
            multiplier_id = multiplier = None

        process = Process(id, name, use, unitcost, unit, quantity, multiplier_id, multiplier)

        # check
        self._assert_equal(process.subtotal, float(line[8]), "process subtotal")

        return process

    def _read_fasteners(self, lines):
        logging.debug("Reading fasteners ... ")

        firstline_index = self._find_line('Fasteners', lines) + 2
        fasteners = []

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            fasteners.append(self._read_fastener(line))

        logging.debug("Reading fasteners ... DONE")
        return fasteners

    def _read_fastener(self, line):
        id = int(line[0])
        name = line[1].strip()
        use = line[2].strip()
        unitcost = float(line[3])

        if line[5].strip():
            size1 = float(line[4])
            unit1 = line[5].strip()
        else:
            size1 = unit1 = None

        if line[7].strip():
            size2 = float(line[6])
            unit2 = line[7].strip()
        else:
            size2 = unit2 = None

        quantity = float(line[8])

        fastener = Fastener(id, name, use, unitcost, size1, unit1, size2, unit2, quantity)

        # check
        self._assert_equal(fastener.subtotal, float(line[9]), "fastener subtotal")

        return fastener

    def _read_toolings(self, lines):
        logging.debug("Reading toolings ...")

        firstline_index = self._find_line('Tooling', lines) + 2
        toolings = []

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            toolings.append(self._read_tooling(line))

        logging.debug("Reading toolings ... DONE")
        return toolings

    def _read_tooling(self, line):
        id = int(line[0])
        name = line[1].strip()
        use = line[2].strip()
        unitcost = float(line[3])
        unit = line[4].strip()
        quantity = float(line[5])
        pvf = float(line[6])

        tooling = Tooling(id, name, use, unitcost, unit, quantity, pvf)

        # check
        self._assert_equal(tooling.subtotal, float(line[8]), "tooling subtotal")

        return tooling

    def _read_drawings(self, filepath):
        logging.debug("Reading drawings...")

        drawings_dir = os.path.abspath(os.path.join(os.path.dirname(filepath), '..', DRAWINGS_DIR))
        logging.debug("Drawings dir: %s" % drawings_dir)

        basename = os.path.splitext(os.path.basename(filepath))[0]

        drawings = glob.glob(os.path.join(drawings_dir, basename + "*.pdf"))
        logging.debug("Found %i drawings" % len(drawings))

        logging.debug("Reading drawings... DONE")
        return drawings

    def _read_pictures(self, filepath):
        logging.debug("Reading pictures...")

        pictures_dir = os.path.abspath(os.path.join(os.path.dirname(filepath), '..', PICTURES_DIR))
        logging.debug("Pictures dir: %s" % pictures_dir)

        basename = os.path.splitext(os.path.basename(filepath))[0]

        pictures = glob.glob(os.path.join(pictures_dir, basename + "*.jpg"))
        logging.debug("Found %i pictures" % len(pictures))

        logging.debug("Reading pictures... DONE")
        return pictures

class PartReader(_ComponentReader):

    def read(self, filepath, system):
        logging.debug("Reading part %s ..." % filepath)

        lines = self._get_lines(filepath)

        header = self._read_header(lines)
        header['system_label'] = system.label

        part = Part(**header)

        self._check_filename(filepath, part.pn)

        part.materials = self._read_materials(lines)
        part.processes = self._read_processes(lines)
        part.fasteners = self._read_fasteners(lines)
        part.toolings = self._read_toolings(lines)

        part.drawings = self._read_drawings(filepath)
        part.pictures = self._read_pictures(filepath)

        system.add_component(part)

        logging.debug("Reading part %s ... DONE" % filepath)
        return part

    def _read_header(self, lines):
        logging.debug("Reading header ...")

        name = lines[3][1].strip()
        pn_base = lines[4][1].strip()
        revision = lines[5][1].strip()
        details = lines[6][1].strip()

        logging.debug("Reading header ... DONE")
        return {'name': name, 'pn_base': pn_base, 'revision': revision,
                'details': details}

class AssemblyReader(_ComponentReader):
    def read(self, filepath, system):
        logging.debug("Reading assembly %s ..." % filepath)

        lines = self._get_lines(filepath)

        header = self._read_header(lines)
        header['system_label'] = system.label

        assembly = Assembly(**header)

        self._check_filename(filepath, assembly.pn)

        assembly.components = self._read_parts(lines, filepath, system)
        assembly.materials = self._read_materials(lines)
        assembly.processes = self._read_processes(lines)
        assembly.fasteners = self._read_fasteners(lines)
        assembly.toolings = self._read_toolings(lines)

        assembly.drawings = self._read_drawings(filepath)
        assembly.pictures = self._read_pictures(filepath)

        # store assembly own quantity in case it does not have any parent
        # in this case, the system reader will take this quantity as being
        # the assembly quantity, otherwise, the parent (system assembly)
        # will determine the assembly quantity
        assembly._user_quantity = self._read_quantity(lines)

        system.add_component(assembly)

        logging.debug("Reading assembly %s ... DONE" % filepath)
        return assembly

    def _read_header(self, lines):
        logging.debug("Reading header ...")

        name = lines[2][1].strip()
        pn_base = lines[3][1].strip()
        revision = lines[4][1].strip()
        details = lines[5][1].strip()

        logging.debug("Reading header ... DONE")
        return {'name': name, 'pn_base': pn_base, 'revision': revision,
                'details': details}

    def _read_quantity(self, lines):
        return int(lines[1][7])

    def _read_parts(self, lines, filepath, system):
        logging.debug("Reading parts ...")

        firstline_index = self._find_line('Parts', lines) + 2
        parts = {}

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            component, quantity = self._read_part(line, filepath, system)

            if component in parts:
                raise ValueError, "Duplicate of component (%s)" % component

            parts[component] = quantity

        logging.debug("Reading parts ... DONE")
        return parts

    def _read_part(self, line, assy_filepath, system):
        pn = line[0]
        quantity = int(line[3])

        if system.has_component(pn): # component already loaded
            component = system.get_component(pn)
        else: # load component
            filename = pn + ".csv"
            filepath = os.path.join(os.path.dirname(assy_filepath), filename)
            if not os.path.exists(filepath):
                raise ValueError, "Missing component (%s)" % pn

            if PART_PN.match(pn):
                component = PartReader().read(filepath, system)
            elif SUB_ASSY_PN.match(pn):
                component = AssemblyReader().read(filepath, system)
            else:
                raise ValueError, "Unknown type of P/N (%s)" % pn

        # check
        unitcost = component.unitcost
        self._assert_equal(unitcost, float(line[2]), "part unitcost")
        self._assert_equal(unitcost * quantity, float(line[4]), "part subtotal")

        return component, quantity

class SystemReader(object):

    def read(self, basepath, system):
        system_dir = os.path.join(basepath, system.label)
        self._check_dir_structure(system_dir)

        components_dir = os.path.join(system_dir, COMPONENTS_DIR)

        system.clear_components() # reset

        for file in self._find_components(components_dir, SYS_ASSY_PN):
            assy = AssemblyReader().read(file, system)
            assy._quantity = 1

        for file in self._find_components(components_dir, SUB_ASSY_PN):
            pn = os.path.splitext(os.path.basename(file))[0]
            if not system.has_component(pn):
                assy = AssemblyReader().read(file, system)
                assy._quantity = assy._user_quantity

        return system

    def _check_dir_structure(self, system_dir):
        ls = os.listdir(system_dir)

        if not COMPONENTS_DIR in ls:
            raise ValueError, "Directory 'components' is missing from %s" % system_dir

        if not DRAWINGS_DIR in ls:
            raise ValueError, "Directory 'drawings' is missing from %s" % system_dir

        if not PICTURES_DIR in ls:
            raise ValueError, "Directory 'pictures' is missing from %s" % system_dir

    def _find_components(self, components_dir, pattern):
        components = []

        files = glob.glob(os.path.join(components_dir, "*.csv"))
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            if pattern.match(filename):
                components.append(file)

        return components
