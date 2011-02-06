#!/usr/bin/env python
"""
================================================================================
:mod:`system` -- 
================================================================================

.. module:: system
   :synopsis: 

.. inheritance-diagram:: system

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

class System(object):
    """
    The cost report has 8 systems.
    """

    def __init__(self, label, name, letter, colour):
        """
        Creates a new system.
        
        :arg label: two characters label
        :arg name: full name
        :arg letter: single character
        :arg colour: RGB of the colour
        :type colour: tuple
        
        Attributes:
        
            * :attr:`label`: two characters label
            * :attr:`name`: full name
            * :attr:`letter`: single character
            * :attr:`colour`: RGB of the colour
        """
        # arguments
        if len(label) != 2:
            raise ValueError, "The label (%s) must be two characters." % label
        self.label = label.upper()

        self.name = name

        if len(letter) != 1:
            raise ValueError, "The letter (%s) must be one character." % letter
        self.letter = letter

        self.colour = colour

        # extras
        self._components = {}

    def add_component(self, component):
        """
        Adds a component. 
        Raises :class:`ValueError` if the component already exists in the system.
        """
        if component.pn in self._components:
            raise ValueError, "Component (%s) is already in the system." % component
        self._components[component.pn] = component

    def has_component(self, pn):
        return pn in self._components

    def get_component(self, pn):
        return self._components[pn]

    def clear_components(self):
        self._components = {}

    def get_hierarchy(self):
        orphans = []
        for component in self._components.values():
            if not component.parents:
                orphans.append(component)

        hierarchy = []
        for orphan in sorted(orphans, reverse=True):
            for component in orphan.get_hierarchy():
                if component not in hierarchy:
                    hierarchy.append(component)

        return hierarchy


BR = System("BR", "Brake System", "A", (153, 204, 255))
EN = System("EN", "Engine & Drivetrain", "B", (204, 255, 204))
FR = System("FR", "Frame & Body", "C", (255, 153, 204))
EL = System("EL", "Electronics, Controls & Wiring", "D", (255, 204, 153))
MS = System("MS", "Miscellaneous, Fit & Finish", "E", (204, 153, 255))
ST = System("ST", "Steering System", "F", (255, 153, 0))
SU = System("SU", "Suspension System", "G", (255, 255, 0))
WT = System("WT", "heels, Wheels Bearings & Tires", "H", (204, 255, 255))

