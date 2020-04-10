#!/usr/bin/env python
"""
================================================================================
:mod:`xlscsv` -- Converter of XLS/XLSX files to CSV files
================================================================================

.. module:: xlscsv
   :synopsis: Converter of XLS/XLSX files to CSV files

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import re
import os
import sys
import glob
import logging
from optparse import OptionParser

# Third party modules.

# Local modules.

# Globals and constants variables.
PATTERN = re.compile("^([A-Z][A-Z])\-")

try:
    from win32com.client import Dispatch
except ImportError:

    def xlstocsv(input_file, output_dir):
        pass


else:

    def xlstocsv(input_file, output_dir):
        xl = Dispatch("Excel.Application")
        wb = xl.Workbooks.Open(input_file)

        for sheet in wb.Worksheets:
            sheetname = sheet.name

            if PATTERN.match(sheetname):
                logging.debug("Converting %s..." % sheetname)
                sheet.Activate()

                filename = sheetname + ".csv"
                output_path = os.path.normpath(os.path.join(output_dir, filename))

                if os.path.exists(output_path):
                    os.remove(output_path)

                sheet.SaveAs(output_path, 6)  # 6: FileFormat = xlCSV

                logging.debug("Converting %s... DONE" % sheetname)

        wb.Close(False)
        xl.Quit


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    parser = OptionParser()

    parser.add_option(
        "--base-path", action="store", dest="base_path", help="Base path of the systems"
    )
    parser.add_option(
        "--system",
        action="store",
        default=None,
        dest="system",
        help="System to convert xlsx to csv",
    )

    options, args = parser.parse_args()

    if not options.base_path:
        parser.print_help()
        sys.exit(1)

    base_path = os.path.abspath(options.base_path)
    logging.info("Base path: %s" % base_path)

    if options.system:
        systems = [options.system]
    else:
        systems = ["BR", "EN", "FR", "EL", "MS", "ST", "SU", "WT"]
    logging.info("Looking through system(s): %s" % ",".join(systems))

    for system in systems:
        dir = os.path.join(base_path, system)
        output_dir = os.path.join(dir, "components")

        for input_file in glob.glob(os.path.join(dir, "*.xls*")):
            logging.info("Converting %s..." % input_file)
            xlstocsv(input_file, output_dir)
            logging.info("Converting %s... DONE" % input_file)
