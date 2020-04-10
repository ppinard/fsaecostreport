#!/usr/bin/env python
"""
Metadata related to the cost report
"""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.


class Metadata(object):
    def __init__(
        self,
        year,
        car_number,
        university,
        team_name,
        competition_name,
        competition_abbrev,
        introduction,
        sae_parts,
        systems,
    ):
        self.year = year
        self.car_number = car_number
        self.university = university
        self.team_name = team_name

        self.competition_name = competition_name
        self.competition_abbrev = competition_abbrev

        self.introduction = introduction
        self.sae_parts = dict(sae_parts)
        self.systems = list(systems)

    @property
    def filename(self):
        return (
            str(self.car_number).zfill(3)
            + "_"
            + self.university
            + "_"
            + self.competition_abbrev
            + "_CR"
        )
