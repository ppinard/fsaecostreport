#!/usr/bin/env python
"""
================================================================================
:mod:`latex` -- Utilities used to create LaTeX output
================================================================================

.. module:: latex
   :synopsis: Utilities used to create LaTeX output

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import glob
import re

# Third party modules.

# Local modules.

# Globals and constants variables.

_latex_special_chars = {
    u'$':  u'\\$',
    u'%':  u'\\%',
    u'&':  u'\\&',
    u'#':  u'\\#',
    u'_':  u'\\_',
    u'{':  u'\\{',
    u'}':  u'\\}',
    u'[':  u'{[}',
    u']':  u'{]}',
    u'"':  u"{''}",
    u'\\': u'\\textbackslash{}',
    u'~':  u'\\textasciitilde{}',
    u'<':  u'\\textless{}',
    u'>':  u'\\textgreater{}',
    u'^':  u'\\textasciicircum{}',
    u'`':  u'{}`', # avoid ?` and !`
    u'\n': u'\\\\',
}

def escape(s):
    r'''
    From Volker Grabsch, python-tex package 1.7
    http://www.profv.de/python-tex/
    
    Escape a unicode string for LaTeX.
    '''
    return u''.join(_latex_special_chars.get(c, c) for c in s)

def create_tabular(data, environment='tabular',
                   tableparameters=None, tablespec=None,
                   format_before_tabular=r'\hline\hline',
                   format_after_tabular='\hline', format_between_rows='',
                   format_after_header=r'\hline', header_endrow=0):
    """
    Create a tabular environment based on the data and the format given.
    """
    tabular = []

    # begin environment
    begin = r'\begin{%s}' % environment
    if tableparameters is not None:
        begin += '[%s]' % tableparameters
    if tablespec is None:
        maxcolumn = max([len(row) for row in data])
        tablespec = 'c' * maxcolumn
    begin += '{%s}' % tablespec

    tabular += [begin]

    # before tabular
    tabular += ['%s' % format_before_tabular]

    #Write data
    for i, row in enumerate(data):
        line = ' & '.join([str(column) for column in row])

        line += r'\tabularnewline%s' % format_between_rows

        if i + 1 == header_endrow:
            line += format_after_header

        tabular += [line]

    #End tabular
    tabular += ['%s' % format_after_tabular]
    tabular += [r'\end{%s}' % environment]

    return tabular

class AuxReader(object):
    def read(self, basepath):
        files = glob.glob(os.path.join(basepath, "*.aux"))
        if not files:
            return {}

        newlabel_lines = []
        with open(files[0], 'r') as f:
            for line in f.readlines():
                if line.startswith("\\newlabel{ct:"):
                    newlabel_lines.append(line.strip())

        pagerefs = {}
        for line in newlabel_lines:
            pn = line[13:24]
            page = int(re.findall('{(\d+)}', line)[0])
            pagerefs.setdefault(pn, page)

        return pagerefs

