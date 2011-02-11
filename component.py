#!/usr/bin/env python
"""
================================================================================
:mod:`component` -- Main objects of the systems: Part and Assembly
================================================================================

.. module:: component
   :synopsis: Main objects of the systems: Part and Assembly

.. inheritance-diagram:: costreport.component

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
from fsaecostreport.pattern import SYS_ASSY_PN, SUB_ASSY_PN, PART_PN

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
            
            * :attr:`parents`: parent assemblies of this component
            * :attr:`components`: parts or assemblies of this component
            
            * :attr:`quantity`: quantity of this component in the whole system
            * :attr:`unitcost`: cost for one of this component
        
        **Notes**:
        
            * Two components are equal if their part number is equal.
        """
        # arguments
        self.filepath = filepath
        self._system_label = system_label.upper()
        self.name = name
        self.pn_base = pn_base.upper()
        self.revision = revision.upper()

        self.details = details

        # extras
        self._quantity = 0
        self.parents = set()
        self.components = {}

        self.materials = []
        self.processes = []
        self.fasteners = []
        self.toolings = []

        self.drawings = []
        self.pictures = []

        # check
        self._validate_pn()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.pn)

    def __eq__(self, other):
        return self.pn == other.pn

    def __ne__(self, other):
        return not self.pn == other.pn

    def __cmp__(self, other):
        # system label
        c = cmp(self._system_label, other._system_label) * -1
        if c != 0:
            return c

        # assembly or part number
        if self.pn_base[0] != other.pn_base[0]:
            if self.pn_base[0] == 'A':
                return 1
            else:
                return - 1

        # designation
        if self.pn_base[1] != other.pn_base[1]:
            if self.pn_base[1] == '0':
                return - 1
            else:
                return cmp(self.pn_base[1] , other.pn_base[1])

        # category
        c = cmp(self.pn_base[2], other.pn_base[2])
        if c != 0:
            return c

        # counter
        c = cmp(int(self.pn_base[3:5]), int(other.pn_base[3:5]))
        if c != 0:
            return c

        # revision
        return cmp(self.revision, other.revision)

    def __hash__(self):
        return hash(self.partnumber)

    def _validate_pn(self):
        return SYS_ASSY_PN.match(self.pn) or \
                SUB_ASSY_PN.match(self.pn) or \
                PART_PN.match(self.pn)

    @property
    def partnumber(self):
        return '%s-%s-%s' % (self._system_label, self.pn_base, self.revision)

    pn = partnumber

    @property
    def quantity(self):
        """
        Returns the overall quantity of this component in a system.
        """
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

        for component, quantity in self.components.iteritems():
            cost += component.unitcost * quantity

        return cost

    def get_hierarchy(self):
        """
        Returns an ordered list of this component and its sub-components.
        """
        hierarchy = [self]

        for component in sorted(self.components.keys(), reverse=True):
            hierarchy.extend(component.get_hierarchy())

        return hierarchy

class Part(_Component):
    """
    A part.
    """
    pass

class Assembly(_Component):
    """
    An assembly.
    """
    pass
