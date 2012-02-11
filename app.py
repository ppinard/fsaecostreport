#!/usr/bin/env python
"""
================================================================================
:mod:`app` -- Command line interface to interact with the cost report's scripts
================================================================================

.. module:: app
   :synopsis: Command line interface to interact with the cost report's scripts

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import logging
import glob
from optparse import OptionParser

# Third party modules.

# Local modules.
from fsaecostreport.xlscsv import xlstocsv
from fsaecostreport.reader import SystemFileReader, MetadataReader
from fsaecostreport.writer import CostReportLaTeXWriter, eBOMWriter

# Globals and constants variables.
from fsaecostreport.system import SYSTEMS

logging.getLogger().setLevel(logging.DEBUG)

def _read(basepath, systems_labels):
    # read systems
    for system_label in systems_labels:
        logging.info("Reading system %s..." % system_label)
        SystemFileReader().read(basepath, SYSTEMS[system_label])
        logging.info("Reading system %s... DONE" % system_label)

    # read metadata
    logging.info("Reading metadata...")
    metadata = MetadataReader().read(basepath)
    logging.info("Reading metadata... DONE")

    return metadata

def run():
    parser = OptionParser()

    parser.add_option('-b', '--basepath', action="store",
                      dest='basepath', default=os.curdir,
                      help="Base path of the cost report (i.e. folder containing the systems) [default=current directory]")

    parser.add_option('-x', '--xlsx2csv', action="store_true",
                      dest='xlsx2csv', default=False,
                      help="Convert the Excel spreadsheets in CSV files")

    parser.add_option('-r', '--read', action="store_true",
                      dest='read', default=False,
                      help="Read the CSVs, drawings and pictures and check for errors")

    parser.add_option('-w', '--write', action="store_true",
                      dest='write', default=False,
                      help="Read, process and write the cost report")

    parser.add_option('-e', '--ebom', action="store_true",
                      dest='ebom', default=False,
                      help="Read, process and write the eBOM")

    options, args = parser.parse_args()

    # basepath
    basepath = os.path.abspath(options.basepath)
    logging.info("Base path: %s" % basepath)

    # systems
    systems_labels = []
    if args:
        for arg in args:
            if arg in SYSTEMS.keys():
                systems_labels.append(arg)
            else:
                logging.error("Unknown system: %s" % arg)
                logging.error("Possible systems: %s" % ','.join(SYSTEMS.keys()))
    else:
        systems_labels = SYSTEMS.keys()
    logging.info("Looking through system(s): %s" % ','.join(systems_labels))

    if options.xlsx2csv:
        for system_label in systems_labels:
            dir = os.path.join(basepath, system_label)
            output_dir = os.path.join(dir, 'components')

            for input_file in glob.glob(os.path.join(dir, '*.xls*')):
                logging.info("Converting %s..." % input_file)
                xlstocsv(input_file, output_dir)
                logging.info("Converting %s... DONE" % input_file)

    elif options.read:
        _read(basepath, systems_labels)

    elif options.write:
        metadata = _read(basepath, systems_labels)

        # write cost report
        logging.info("Writing cost report...")
        CostReportLaTeXWriter().write(basepath, SYSTEMS.values(), metadata)
        logging.info("Writing cost report... DONE")

    elif options.ebom:
        metadata = _read(basepath, systems_labels)

        # write eBOM
        logging.info("Writing eBOM...")
        eBOMWriter().write(basepath, SYSTEMS.values(), metadata)
        logging.info("Writing eBOM... DONE")

    else:
        parser.print_help()

if __name__ == '__main__':
    run()
