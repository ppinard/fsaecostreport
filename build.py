#!/usr/bin/env python
"""
================================================================================
:mod:`build` -- Distribution builder
================================================================================

.. module:: build
   :synopsis: Distribution builder

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os

# Third party modules.

# Local modules.
from setuputilities.builder import SetupBuild, BaseBuild, DocBuild, TestBuild
from setuputilities.builder.py2exe import Py2exeBuild
from setuputilities.util import find_package_path, find_packages, find_package_data

# Globals and constants variables.

class Build(BaseBuild, SetupBuild, DocBuild, TestBuild, Py2exeBuild):
    PROJECT_DIR = find_package_path('costreport')

    def __init__(self):
        BaseBuild.__init__(self)
        SetupBuild.__init__(self)
        DocBuild.__init__(self)
        TestBuild.__init__(self)
        Py2exeBuild.__init__(self)

        # Base Build
        self.metadata.name = "costreport"
        self.metadata.version = "0.1"
        self.metadata.author = "Philippe T. Pinard"
        self.metadata.author_email = "philippe.pinard@gmail.com"
        self.metadata.description = "Generator of the FSAE Cost Report"
        self.metadata.license = "GPL v3"
        self.metadata.classifiers = [
                "Development Status :: 4 - Beta",
                "License :: OSI Approved :: GNU General Public License (GPL)",
                "Natural Language :: English",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Topic :: Software Development"]
        self.metadata.platforms = "Windows OS"

        # Setup Build
        self.packages = find_packages("costreport",
                                      where=self.PROJECT_DIR)
        self.package_data = find_package_data(package='costreport',
                                              where=self.PROJECT_DIR)

        # Doc Build
        self.doc_dir = os.path.join(self.PROJECT_DIR, 'docs')

        # py2exe
        self.console_script = [os.path.join(self.PROJECT_DIR, 'app.py')]

if __name__ == '__main__':
    build = Build()
    build.run()
