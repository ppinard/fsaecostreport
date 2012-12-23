#!/usr/bin/env python
"""
================================================================================
:mod:`pattern` -- Regex patterns used to identify part numbers
================================================================================

.. module:: pattern
   :synopsis: Regex patterns used to identify part numbers

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import re

# Third party modules.

# Local modules.

# Globals and constants variables.

PART_PN = re.compile('([A-Z][A-Z])\-(00\d\d\d)\-([A-Z][A-Z])')
SUB_ASSY_PN = re.compile('([A-Z][A-Z])\-(A0\d\d\d)\-([A-Z][A-Z])')
SYS_ASSY_PN = re.compile('([A-Z][A-Z])\-(A\d\d00)\-([A-Z][A-Z])')
