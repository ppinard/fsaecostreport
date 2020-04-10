#!/usr/bin/env python
"""
================================================================================
:mod:`costtable` -- Items in the cost tables: material, process, etc.
================================================================================

.. module:: costtable
   :synopsis: Items in the cost tables: material, process, etc.

.. inheritance-diagram:: fsaecostreport.costtable

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


class _CostTableItem(object):
    def __init__(self, id, name, use, unitcost, quantity):
        self.id = id
        self.name = name
        self.use = use
        self.unitcost = unitcost
        self.quantity = quantity

    def __str__(self):
        return self.name

    @property
    def subtotal(self):
        return self.quantity * self.unitcost


class Material(_CostTableItem):
    def __init__(self, id, name, use, unitcost, size1, unit1, size2, unit2, quantity):
        _CostTableItem.__init__(self, id, name, use, unitcost, quantity)

        self.size1 = size1
        self.unit1 = unit1
        self.size2 = size2
        self.unit2 = unit2


class Process(_CostTableItem):
    def __init__(
        self, id, name, use, unitcost, unit, quantity, multiplier_id, multiplier
    ):
        _CostTableItem.__init__(self, id, name, use, unitcost, quantity)

        self.unit = unit
        self.multiplier_id = multiplier_id
        self.multiplier = multiplier

    @property
    def subtotal(self):
        if self.multiplier_id:
            return self.quantity * self.unitcost * self.multiplier
        else:
            return self.quantity * self.unitcost


class Fastener(_CostTableItem):
    def __init__(self, id, name, use, unitcost, size1, unit1, size2, unit2, quantity):
        _CostTableItem.__init__(self, id, name, use, unitcost, quantity)

        self.size1 = size1
        self.unit1 = unit1
        self.size2 = size2
        self.unit2 = unit2


class Tooling(_CostTableItem):
    def __init__(self, id, name, use, unitcost, unit, quantity, pvf):
        _CostTableItem.__init__(self, id, name, use, unitcost, quantity)

        self.unit = unit
        self.pvf = pvf

    @property
    def subtotal(self):
        return self.unitcost * self.quantity / self.pvf
