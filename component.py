#!/usr/bin/env python
"""
================================================================================
:mod:`component` -- 
================================================================================

.. module:: component
   :synopsis: 

.. inheritance-diagram:: component

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
from pattern import PN_BASE

# Globals and constants variables.

class _Component(object):
    """
    Abstract class for parts and assemblies.
    """
    def __init__(self, filepath, system_label, name, pn_base, revision, details=''):
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
        self.filepath = filepath

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
        self._quantity = 0
        self.parents = set()

        self.materials = []
        self.processes = []
        self.fasteners = []
        self.toolings = []

        self.drawings = []
        self.pictures = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.pn)

    def __eq__(self, other):
        return self.partnumber == other.partnumber

    def __cmp__(self, other):
        #TODO: component comparison
        return cmp(self.partnumber, other.partnumber)

    def __hash__(self):
        return hash(self.partnumber)

    def _validate_pn_base(self, pn_base):
        return bool(PN_BASE.match(pn_base))

    @property
    def partnumber(self):
        return '%s-%s-%s' % (self._system_label, self.pn_base, self.revision)

    pn = partnumber

    @property
    def quantity(self):
        if not self.parents:
            return self._quantity
        else:
            qty = 0
            for parent in self.parents:
                qty += parent.quantity * parent.components[self]
            return qty

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

    def __init__(self, filepath, system_label, name, pn_base, revision, details=''):
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
        _Component.__init__(self, filepath, system_label, name, pn_base, revision, details)

        # extras
        self.components = {}
        self._quantity = 0

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
