#!/usr/bin/env python
"""
Regex patterns used to identify part numbers
"""

# Standard library modules.
import re


# Local modules.

# Globals and constants variables.

PART_PN = re.compile("([A-Z][A-Z])\-(00\d\d\d)\-([A-Z][A-Z])")
SUB_ASSY_PN = re.compile("([A-Z][A-Z])\-(A0\d\d\d)\-([A-Z][A-Z])")
SYS_ASSY_PN = re.compile("([A-Z][A-Z])\-(A\d000)\-([A-Z][A-Z])")
