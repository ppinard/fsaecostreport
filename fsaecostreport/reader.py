#!/usr/bin/env python
"""
File readers for systems, parts, assemblies and metadata
"""

# Standard library modules.
import csv
import os.path
import logging
import glob
import re
from configparser import ConfigParser
import unicodedata
from operator import attrgetter, itemgetter

# Third party modules.

# Local modules.
from fsaecostreport.metadata import Metadata
from fsaecostreport.costtable import Material, Process, Fastener, Tooling
from fsaecostreport.component import Part, Assembly
from fsaecostreport.pattern import SYS_ASSY_PN, SUB_ASSY_PN, PART_PN
from fsaecostreport.system import System

# Globals and constants variables.
from fsaecostreport.constants import (
    COMPONENTS_DIR,
    DRAWINGS_DIR,
    PICTURES_DIR,
    CONFIG_FILE,
    INTRODUCTION_FILE,
    SAE_PARTS_FILE,
)

COMMA_SPLIT_PATTERN = re.compile(r"[^,;\s]+")


def ascii(unistr):
    """
    Convert unicode to ascii.
    """
    try:
        if isinstance(unistr, str):
            ascii_chrs = []

            for char in unistr:
                decomposition = unicodedata.decomposition(char)

                try:
                    root, _modifier = decomposition.split()
                except:  # Not a unicode character
                    ascii_chrs.append(char)
                else:  # Convert to ascii
                    try:
                        ascii_chr = chr(int(root, 16))  # root is in hex base
                        ascii_chrs.append(ascii_chr)
                    except:
                        pass

            return "".join(ascii_chrs)
        else:
            return unistr
    except Exception as ex:
        raise Exception("Reading %s: %s" % (unistr, str(ex)))


class _ComponentFileReader(object):
    def _read(self, component, lines):
        self._check_filename(component.filepath, component.pn)

        component.materials = self._read_materials(lines)
        component.processes = self._read_processes(lines)
        component.fasteners = self._read_fasteners(lines)
        component.toolings = self._read_toolings(lines)

        component.drawings = self._read_drawings(component.filepath)
        component.pictures = self._read_pictures(component.filepath)

    def _get_lines(self, filepath):
        logging.debug("Reading csv")
        reader = csv.reader(open(filepath, "r"))
        logging.debug("Reading csv... DONE")
        return list(reader)

    def _find_line(self, lookup, lines):
        firstcol_getter = itemgetter(0)
        firstcol = list(map(firstcol_getter, lines))

        return firstcol.index(lookup)

    def _assert_equal(self, a, b, context="", places=4):
        if round(abs(b - a), places) != 0:
            raise AssertionError(context + ": %s != %s" % (a, b))

    def _check_filename(self, filepath, pn):
        filename = os.path.splitext(os.path.basename(filepath))[0]
        if filename != pn:
            raise AssertionError("filename (%s) != part number (%s)" % (filename, pn))

    def _read_materials(self, lines):
        logging.debug("Reading materials ...")

        firstline_index = self._find_line("Materials", lines) + 2
        materials = []

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            materials.append(self._read_material(line))

        logging.debug("Reading materials ... DONE")
        return materials

    def _read_material(self, line):
        id = int(line[0])
        name = ascii(line[1].strip())
        use = ascii(line[2].strip())
        unitcost = float(line[3])

        if line[5].strip():
            size1 = float(line[4])
            unit1 = ascii(line[5].strip())
        else:
            size1 = unit1 = None

        if line[7].strip():
            size2 = float(line[6])
            unit2 = ascii(line[7].strip())
        else:
            size2 = unit2 = None

        quantity = float(line[8])

        material = Material(
            id, name, use, unitcost, size1, unit1, size2, unit2, quantity
        )

        # check
        self._assert_equal(material.subtotal, float(line[9]), "material subtotal")

        return material

    def _read_processes(self, lines):
        logging.debug("Reading processes ...")

        firstline_index = self._find_line("Processes", lines) + 2
        processes = []

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            processes.append(self._read_process(line))

        logging.debug("Reading processes ... DONE")
        return processes

    def _read_process(self, line):
        id = int(line[0])
        name = ascii(line[1].strip())
        use = ascii(line[2].strip())
        unitcost = float(line[3])
        unit = ascii(line[4].strip())
        quantity = float(line[5])

        if line[6].strip():
            multiplier_id = int(line[6])
            multiplier = float(line[7])
        else:
            multiplier_id = multiplier = None

        process = Process(
            id, name, use, unitcost, unit, quantity, multiplier_id, multiplier
        )

        # check
        self._assert_equal(process.subtotal, float(line[8]), "process subtotal")

        return process

    def _read_fasteners(self, lines):
        logging.debug("Reading fasteners ... ")

        firstline_index = self._find_line("Fasteners", lines) + 2
        fasteners = []

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            fasteners.append(self._read_fastener(line))

        logging.debug("Reading fasteners ... DONE")
        return fasteners

    def _read_fastener(self, line):
        id = int(line[0])
        name = ascii(line[1].strip())
        use = ascii(line[2].strip())
        unitcost = float(line[3])

        if line[5].strip():
            size1 = float(line[4])
            unit1 = ascii(line[5].strip())
        else:
            size1 = unit1 = None

        if line[7].strip():
            size2 = float(line[6])
            unit2 = ascii(line[7].strip())
        else:
            size2 = unit2 = None

        quantity = float(line[8])

        fastener = Fastener(
            id, name, use, unitcost, size1, unit1, size2, unit2, quantity
        )

        # check
        self._assert_equal(fastener.subtotal, float(line[9]), "fastener subtotal")

        return fastener

    def _read_toolings(self, lines):
        logging.debug("Reading toolings ...")

        firstline_index = self._find_line("Tooling", lines) + 2
        toolings = []

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            toolings.append(self._read_tooling(line))

        logging.debug("Reading toolings ... DONE")
        return toolings

    def _read_tooling(self, line):
        id = int(line[0])
        name = ascii(line[1].strip())
        use = ascii(line[2].strip())
        unitcost = float(line[3])
        unit = ascii(line[4].strip())
        quantity = float(line[5])
        pvf = float(line[6])

        tooling = Tooling(id, name, use, unitcost, unit, quantity, pvf)

        # check
        self._assert_equal(tooling.subtotal, float(line[8]), "tooling subtotal")

        return tooling

    def _read_drawings(self, filepath):
        logging.debug("Reading drawings...")

        drawings_dir = os.path.abspath(
            os.path.join(os.path.dirname(filepath), "..", DRAWINGS_DIR)
        )
        logging.debug("Drawings dir: %s" % drawings_dir)

        basename = os.path.splitext(os.path.basename(filepath))[0]

        drawings = glob.glob(os.path.join(drawings_dir, basename + "*.pdf"))
        logging.debug("Found %i drawings" % len(drawings))

        logging.debug("Reading drawings... DONE")
        return drawings

    def _read_pictures(self, filepath):
        logging.debug("Reading pictures...")

        pictures_dir = os.path.abspath(
            os.path.join(os.path.dirname(filepath), "..", PICTURES_DIR)
        )
        logging.debug("Pictures dir: %s" % pictures_dir)

        basename = os.path.splitext(os.path.basename(filepath))[0]

        pictures = glob.glob(os.path.join(pictures_dir, basename + "*.jpg"))
        logging.debug("Found %i pictures" % len(pictures))

        logging.debug("Reading pictures... DONE")
        return pictures


class PartFileReader(_ComponentFileReader):
    def read(self, filepath, system):
        logging.debug("Reading part %s ..." % filepath)

        lines = self._get_lines(filepath)

        header = self._read_header(lines)
        header["system_label"] = system.label

        part = Part(filepath, **header)
        self._read(part, lines)

        system.add_component(part)

        logging.debug("Reading part %s ... DONE" % filepath)
        return part

    def _read_header(self, lines):
        logging.debug("Reading header ...")

        name = ascii(lines[3][1].strip())
        pn_base = ascii(lines[4][1].strip())
        revision = ascii(lines[5][1].strip())
        details = ascii(lines[6][1].strip())

        logging.debug("Reading header ... DONE")
        return {
            "name": name,
            "pn_base": pn_base,
            "revision": revision,
            "details": details,
        }


class AssemblyFileReader(_ComponentFileReader):
    def read(self, filepath, system):
        logging.debug("Reading assembly %s ..." % filepath)

        lines = self._get_lines(filepath)

        header = self._read_header(lines)
        header["system_label"] = system.label

        assembly = Assembly(filepath, **header)
        self._read(assembly, lines)

        # store assembly own quantity in case it does not have any parent
        # in this case, the system reader will take this quantity as being
        # the assembly quantity, otherwise, the parent (system assembly)
        # will determine the assembly quantity
        assembly._quantity = self._read_quantity(lines)

        assembly.components = self._read_parts(lines, assembly, system)

        system.add_component(assembly)

        logging.debug("Reading assembly %s ... DONE" % filepath)
        return assembly

    def _read_header(self, lines):
        logging.debug("Reading header ...")

        name = ascii(lines[2][1].strip())
        pn_base = ascii(lines[3][1].strip())
        revision = ascii(lines[4][1].strip())
        details = ascii(lines[5][1].strip())

        logging.debug("Reading header ... DONE")
        return {
            "name": name,
            "pn_base": pn_base,
            "revision": revision,
            "details": details,
        }

    def _read_quantity(self, lines):
        return int(lines[1][7])

    def _read_parts(self, lines, assembly, system):
        logging.debug("Reading parts ...")

        firstline_index = self._find_line("Parts", lines) + 2
        parts = {}

        for line in lines[firstline_index:]:
            if not line[0].strip():
                break

            component, quantity = self._read_part(line, assembly, system)

            if component in parts:
                raise ValueError("Duplicate of component (%s)" % component)

            parts[component] = quantity

        logging.debug("Reading parts ... DONE")
        return parts

    def _read_part(self, line, assembly, system):
        pn = line[0]
        quantity = int(line[3])

        if system.has_component(pn):  # component already loaded
            component = system.get_component(pn)
        else:  # load component
            filename = pn + ".csv"
            filepath = os.path.join(os.path.dirname(assembly.filepath), filename)
            if not os.path.exists(filepath):
                raise ValueError("Missing component (%s)" % pn)

            if PART_PN.match(pn):
                component = PartFileReader().read(filepath, system)
            elif SUB_ASSY_PN.match(pn):
                component = AssemblyFileReader().read(filepath, system)
            else:
                raise ValueError("Unknown type of P/N (%s)" % pn)

        component.parents.add(assembly)

        # check
        unitcost = component.unitcost
        self._assert_equal(unitcost, float(line[2]), "part unitcost")
        self._assert_equal(unitcost * quantity, float(line[4]), "part subtotal")

        return component, quantity


class SystemFileReader(object):
    def read(self, basepath, system):
        system_dir = os.path.join(basepath, system.label)
        self._check_dir_structure(system_dir)

        components_dir = os.path.join(system_dir, COMPONENTS_DIR)

        system.clear_components()  # reset

        for file in self._find_components(components_dir, SYS_ASSY_PN):
            AssemblyFileReader().read(file, system)

        for file in self._find_components(components_dir, SUB_ASSY_PN):
            pn = os.path.splitext(os.path.basename(file))[0]
            if not system.has_component(pn):
                AssemblyFileReader().read(file, system)

        # check
        self._check_unread_components(basepath, system)
        self._check_unread_drawings(basepath, system)
        self._check_unread_pictures(basepath, system)

        return system

    def _check_dir_structure(self, system_dir):
        ls = os.listdir(system_dir)

        if not COMPONENTS_DIR in ls:
            raise ValueError("Directory 'components' is missing from %s" % system_dir)

        if not DRAWINGS_DIR in ls:
            raise ValueError("Directory 'drawings' is missing from %s" % system_dir)

        if not PICTURES_DIR in ls:
            raise ValueError("Directory 'pictures' is missing from %s" % system_dir)

    def _check_unread_components(self, basepath, system):
        filepath_getter = attrgetter("filepath")

        expected = map(filepath_getter, system._components.values())
        actual = glob.glob(os.path.join(basepath, COMPONENTS_DIR, "*.csv"))

        diff = set(actual) - set(expected)

        if diff:
            msg = "The following components were not read:\n"
            for filepath in diff:
                msg += "  - %s\n" % filepath

            raise ValueError(msg)

    def _check_unread_drawings(self, basepath, system):
        expected = []
        for component in system._components.values():
            expected.extend(component.drawings)

        actual = glob.glob(os.path.join(basepath, DRAWINGS_DIR, "*.pdf"))

        diff = set(actual) - set(expected)

        if diff:
            msg = "The following drawings were not read:\n"
            for filepath in diff:
                msg += "  - %s\n" % filepath

            raise ValueError(msg)

    def _check_unread_pictures(self, basepath, system):
        expected = []
        for component in system._components.values():
            expected.extend(component.pictures)

        actual = glob.glob(os.path.join(basepath, PICTURES_DIR, "*.jpg"))

        diff = set(actual) - set(expected)

        if diff:
            msg = "The following drawings were not read:\n"
            for filepath in diff:
                msg += "  - %s\n" % filepath

            raise ValueError(msg)

    def _find_components(self, components_dir, pattern):
        components = []

        files = glob.glob(os.path.join(components_dir, "*.csv"))
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            if pattern.match(filename):
                components.append(file)

        return components


class MetadataReader(object):
    def read(self, basepath):
        filepath = os.path.join(basepath, CONFIG_FILE)
        if not os.path.exists(filepath):
            raise IOError("No configuration file")

        parser = ConfigParser()
        parser.read(filepath)

        year = int(parser.get("CostReport", "year"))
        car_number = int(parser.get("CostReport", "carnumber"))
        university = ascii(parser.get("CostReport", "university"))
        team_name = ascii(parser.get("CostReport", "teamname"))
        competition_name = ascii(parser.get("CostReport", "competitionname"))
        competition_abbrev = ascii(parser.get("CostReport", "competitionabbrev"))
        introduction = self._read_introduction(basepath)

        # Systems
        system_labels = parser.get("CostReport", "systems")
        system_labels = COMMA_SPLIT_PATTERN.findall(system_labels)

        systems = []
        for label in system_labels:
            if not parser.has_section(label):
                raise ValueError("No section for system: %s" % label)

            order = int(parser.get(label, "order"))
            name = parser.get(label, "name")
            colour = parser.get(label, "colour")
            colour = COMMA_SPLIT_PATTERN.findall(colour)
            colour = map(int, colour)
            colour = tuple(colour)

            system = System(order, label, name, colour)
            systems.append(system)

        systems = sorted(systems)  # Sort by letters

        sae_parts = self._read_sae_parts(basepath, systems)

        return Metadata(
            year,
            car_number,
            university,
            team_name,
            competition_name,
            competition_abbrev,
            introduction,
            sae_parts,
            systems,
        )

    def _read_introduction(self, basepath):
        lines = []
        with open(os.path.join(basepath, INTRODUCTION_FILE), "r") as f:
            for line in f.readlines():
                lines.append(ascii(line.strip()))
        return lines

    def _read_sae_parts(self, basepath, systems):
        # Empty SAE parts
        sae_parts = {}
        for system in systems:
            sae_parts.setdefault(system, [])

        # Check file existence
        filepath = os.path.join(basepath, SAE_PARTS_FILE)
        if not os.path.exists(filepath):
            raise IOError("No SAE common parts file")

        # Look-up table for system labels
        keys = map(attrgetter("label"), systems)
        systems_ref = dict(zip(keys, systems))

        # Read file
        with open(filepath, "r") as fp:
            reader = csv.reader(fp)

            for row in reader:
                try:
                    system = systems_ref[row[0].strip()]
                except KeyError:
                    continue

                component_name = row[1].strip()
                pn = row[2].strip()
                if pn:
                    if not (
                        PART_PN.match(pn)
                        or SYS_ASSY_PN.match(pn)
                        or SUB_ASSY_PN.match(pn)
                    ):
                        raise ValueError(
                            "Part number for %s is invalid" % component_name
                        )
                else:
                    pn = None

                sae_parts[system].append((component_name, pn))

        return sae_parts
