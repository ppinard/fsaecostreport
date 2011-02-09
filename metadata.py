#!/usr/bin/env python
"""
================================================================================
:mod:`metadata` -- 
================================================================================

.. module:: metadata
   :synopsis: 

.. inheritance-diagram:: metadata

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2011 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class Metadata(object):
    def __init__(self, year, car_number, university, team_name, introduction):
        self.year = year
        self.car_number = car_number
        self.university = university
        self.team_name = team_name
        self.introduction = introduction
