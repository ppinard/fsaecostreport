#!/usr/bin/env python
"""
================================================================================
:mod:`compare` -- Compare cost tables between years
================================================================================

.. module:: compare
   :synopsis: Compare cost tables between years

.. inheritance-diagram:: fsaecostreport.compare

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import csv
import logging
from operator import itemgetter
from argparse import ArgumentParser

# Third party modules.
import xlrd

# Local modules.

# Globals and constants variables.

class Comparator(object):

    def __init__(self, filepath1, filepath2, outfilepath):
        self._rows1 = self._read(filepath1)
        self._rows2 = self._read(filepath2)
        self._outfilepath = outfilepath

    def _read(self, filepath):
        ext = os.path.splitext(filepath)[1]

        if ext == '.csv':
            return self._read_csv(filepath)
        elif ext == '.xls':
            return self._read_xls(filepath)
        else:
            raise ValueError, 'Unknown extension: %s' % ext

    def _read_csv(self, filepath):
        logging.debug("Reading %s", filepath)

        with open(filepath, 'r') as fp:
            reader = csv.reader(fp)
            rows = list(reader)

        return rows

    def _read_xls(self, filepath):
        logging.debug("Reading %s", filepath)

        wb = xlrd.open_workbook(filepath)
        sheet = wb.sheet_by_index(0)

        rows = []
        for irow in range(sheet.nrows):
            row = []

            for icol in range(sheet.ncols):
                try:
                    row.append(str(sheet.cell(irow, icol).value))
                except UnicodeEncodeError:
                    raise ValueError, 'UnicodeEncodeError at row %i col %i' % (irow, icol)

            rows.append(row)

        return rows

    def compare(self):
        rows = []
        names1 = map(itemgetter(1), self._rows1)

        for row2 in self._rows2:
            # Find row in rows2
            try:
                irow1 = names1.index(row2[1])
                id = self._rows1[irow1][0]
            except:
                print 'No matching row for "%s"' % row2[1]
                id = ''

            rows.append([id, row2[1]])

        with open(self._outfilepath, 'w') as fp:
            writer = csv.writer(fp)
            writer.writerows(rows)
#
def run():
    desc = 'Compare two different cost tables'
    parser = ArgumentParser(description=desc)

    parser.add_argument('oldfilepath', metavar='OLD_FILEPATH',
                        help='Location of old cost table')
    parser.add_argument('newfilepath', metavar='NEW_FILEPATH',
                        help='Location of new cost table')
    parser.add_argument('-o', dest='outfilepath', required=True,
                        metavar='OUT_FILEPATH', help='Output file')

    args = parser.parse_args()

    comparator = Comparator(args.oldfilepath, args.newfilepath, args.outfilepath)
    comparator.compare()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    run()
