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
import operator

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

BR = System("BR", "Brake System", "A", (153, 204, 255))
EN = System("EN", "Engine & Drivetrain", "B", (204, 255, 204))
FR = System("FR", "Frame & Body", "C", (255, 153, 204))
EL = System("EL", "Electronics, Controls & Wiring", "D", (255, 204, 153))
MS = System("MS", "Miscellaneous, Fit & Finish", "E", (204, 153, 255))
ST = System("ST", "Steering System", "F", (255, 153, 0))
SU = System("SU", "Suspension System", "G", (255, 255, 0))
WT = System("WT", "heels, Wheels Bearings & Tires", "H", (204, 255, 255))

class _Component(object):
    """
    Abstract class for parts and assemblies.
    """
    def __init__(self, system_label, name, pn_base, revision, details=''):
        """
        Creates a component.
        
        :arg system_label: label of the system in which the component is in
        :arg name: full name
        :arg pn_base: part number base (e.g. 00001 in BR-00001-AA)
        :arg revision: two characters revision
        :arg details: further details/description
        
        **Attributes**:
        
            * :attr:`name`: full name
            * :attr:`pn_base`: part number base (e.g. 00001 in BR-00001-AA)
            * :attr:`revision`: two characters revision
            * :attr:`details`: further details/description
            * :attr:`partnumber` or :attr:`pn`: part number (e.g. BR-00001-AA)
            * :attr:`materials`: list of materials
            * :attr:`processes`: list of processes
            * :attr:`fasteners`: list of fasteners
            * :attr:`toolings`: list of toolings
            * :attr:`drawings`: list of drawings (paths of files)
            * :attr:`pictures`: list of pictures (paths of files)
        
        **Notes**:
        
            * Two components are equal if their part number is equal.
        """
        # arguments
        if len(system_label) != 2:
            raise ValueError, "The system label (%s) must be two characters." % system_label
        self._system_label = system_label.upper()

        self.name = name

        if not self._validate_pn_base(pn_base):
            raise ValueError, "Invalid part number base (%s)." % pn_base
        self.pn_base = pn_base.upper()

        if len(revision) != 2:
            raise ValueError, "The revision (%s) must be two characters." % revision
        self.revision = revision.upper()

        self.details = details

        # extras
        self.materials = []
        self.processes = []
        self.fasteners = []
        self.toolings = []

        self.drawings = []
        self.pictures = []

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.partnumber == other.partnumber

    def __cmp__(self, other):
        #TODO: component comparison
        return cmp(self.partnumber, other.partnumber)

    def __hash__(self):
        return hash(self.partnumber)

    def _validate_pn_base(self, pn_base):
        #TODO: part number validation
        return True

    @property
    def partnumber(self):
        return '%s-%s-%s' % (self._system_label, self.pn_base, self.revision)

    pn = partnumber

    @property
    def unitcost(self):
        """
        Returns the unit cost of the component by adding the subtotal of the
        materials, processes, fasteners and toolings.
        """
        subtotal_getter = operator.attrgetter('subtotal')

        cost = 0.0

        cost += sum(map(subtotal_getter, self.materials))
        cost += sum(map(subtotal_getter, self.processes))
        cost += sum(map(subtotal_getter, self.fasteners))
        cost += sum(map(subtotal_getter, self.toolings))

        return cost

class Part(_Component):
    """
    A part.
    """
    pass

class Assembly(_Component):
    """
    An assembly.
    """

    def __init__(self, system_label, name, pn_base, revision, details=''):
        """
        Creates a component.
        
        :arg system_label: label of the system in which the component is in
        :arg name: full name
        :arg pn_base: part number base (e.g. 00001 in BR-00001-AA)
        :arg revision: two characters revision
        :arg details: further details/description
        
        **Attributes**:
        
            * :attr:`name`: full name
            * :attr:`pn_base`: part number base (e.g. 00001 in BR-00001-AA)
            * :attr:`revision`: two characters revision
            * :attr:`details`: further details/description
            * :attr:`partnumber` or :attr:`pn`: part number (e.g. BR-00001-AA)
            * :attr:`quantity`: overall quantity of the components
            * :attr:`materials`: list of materials
            * :attr:`processes`: list of processes
            * :attr:`fasteners`: list of fasteners
            * :attr:`toolings`: list of toolings
            * :attr:`drawings`: list of drawings (paths of files)
            * :attr:`pictures`: list of pictures (paths of files)
            * :attr:`components`: dictionary of this assembly's parts.
                The keys are the component objects and the values the quantity
                of each part.
        
        **Notes**:
        
            * Two components are equal if their part number is equal.
        """
        _Component.__init__(self, system_label, name, pn_base, revision, details)

        # extras
        self.components = {}
        self._quantity = 0

    @property
    def quantity(self):
        if self._quantity <= 0:
            raise ValueError, "No quantity set. This assembly has a parent."
        return self._quantity

    @property
    def unitcost(self):
        """
        Returns the unit cost of the component by adding the subtotal of the
        materials, processes, fasteners and toolings.
        """
        subtotal_getter = operator.attrgetter('subtotal')

        cost = 0.0

        cost += sum(map(subtotal_getter, self.materials))
        cost += sum(map(subtotal_getter, self.processes))
        cost += sum(map(subtotal_getter, self.fasteners))
        cost += sum(map(subtotal_getter, self.toolings))

        for component, quantity in self.components.iteritems():
            cost += component.unitcost * quantity

        return cost
