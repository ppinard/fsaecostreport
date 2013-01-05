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
from operator import attrgetter

# Third party modules.

# Local modules.
from fsaecostreport.xlscsv import xlstocsv
from fsaecostreport.reader import SystemFileReader, MetadataReader
from fsaecostreport.writer import CostReportLaTeXWriter, eBOMWriter

# Globals and constants variables.

logging.getLogger().setLevel(logging.DEBUG)

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

    # read metadata
    logging.info("Reading metadata...")
    metadata = MetadataReader().read(basepath)
    logging.info("Reading metadata... DONE")

    # systems
    values = metadata.systems
    keys = map(attrgetter('label'), values)
    available_systems = dict(zip(keys, values))

    systems = []
    if args:
        for arg in args:
            try:
                systems.append(available_systems[arg])
            except KeyError:
                parser.error("Unknown system: %s" % arg)
                parser.error("Possible systems: %s" % ','.join(available_systems.keys()))
    else:
        systems = available_systems.values()
    logging.info("Looking through system(s): %s",
                 ', '.join(map(attrgetter('label'), systems)))

    metadata.systems = sorted(systems)

    if options.xlsx2csv:
        for system in metadata.systems:
            dir = os.path.join(basepath, system.label)
            output_dir = os.path.join(dir, 'components')

            for input_file in glob.glob(os.path.join(dir, '*.xls*')):
                logging.info("Converting %s..." % input_file)
                xlstocsv(input_file, output_dir)
                logging.info("Converting %s... DONE" % input_file)

    # read systems
    if options.read or options.write or options.ebom:
        for system in metadata.systems:
            logging.info("Reading system %s..." % system)
            SystemFileReader().read(basepath, system)
            logging.info("Reading system %s... DONE" % system)

    # write cost report
    if options.write:
        logging.info("Writing cost report...")
        CostReportLaTeXWriter().write(basepath, metadata)
        logging.info("Writing cost report... DONE")

    if options.ebom:
        # write eBOM
        logging.info("Writing eBOM...")
        eBOMWriter().write(basepath, metadata)
        logging.info("Writing eBOM... DONE")

if __name__ == '__main__':
    run()
