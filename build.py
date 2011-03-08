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
import zipfile

# Third party modules.
from pkg_resources import to_filename

# Local modules.
from setuputilities.builder.project import Project
from setuputilities.builder.base import BaseBuild
from setuputilities.builder.setup import SetupBuild
from setuputilities.builder.doc import DocBuild
from setuputilities.builder.test import TestBuild
from setuputilities.builder.cover import CoverageBuild
from setuputilities.builder.py2exe import Py2exeBuild
from setuputilities.util import \
    find_package_path, find_packages, find_package_data, cleanup

# Globals and constants variables.

project = Project(find_package_path('fsaecostreport'))

# Base Build
project.metadata.name = "fsaecostreport"
project.metadata.version = "0.2"
project.metadata.author = "Philippe T. Pinard"
project.metadata.author_email = "philippe.pinard@gmail.com"
project.metadata.description = "Generator of the FSAE Cost Report"
project.metadata.license = "GPL v3"
project.metadata.classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development"]
project.metadata.platforms = "Windows OS"

# Setup Build
project.packages = find_packages("fsaecostreport", where=project.dir)
project.package_data = \
    find_package_data(package='fsaecostreport', where=project.dir)
project.data_files = []

# Doc Build
project.doc_dir = os.path.join(project.dir, 'doc')

# py2exe
project.windows_scripts = []
project.console_scripts = [os.path.join(project.dir, 'app.py')]

class Build(BaseBuild, SetupBuild, DocBuild, TestBuild, Py2exeBuild, CoverageBuild):
    def __init__(self, project):
        BaseBuild.__init__(self, project)
        SetupBuild.__init__(self, project)
        DocBuild.__init__(self, project)
        TestBuild.__init__(self, project)
        Py2exeBuild.__init__(self, project)
        CoverageBuild.__init__(self, project)

    def bdist_exe(self):
        Py2exeBuild.bdist_exe(self)

        dest_dir = os.path.join(self.dest_dir, 'exe', self.project.metadata.name)

        # rename app.exe to costreport-app.exe
        old = os.path.join(dest_dir, 'app.exe')
        new = os.path.join(dest_dir, 'costreport-app.exe')
        os.rename(old, new)

        # zip the dest
        zip_dir = os.path.join(self.dest_dir, 'zip', self.project.metadata.name)
        if not os.path.exists(zip_dir):
            os.makedirs(zip_dir)

        zip_filename = '%s-%s.zip' % (to_filename(self.project.metadata.name),
                                      to_filename(self.project.metadata.version))

        zip = zipfile.ZipFile(os.path.join(zip_dir, zip_filename), mode='w')

        # walk through the file and folders in dest
        for root, _dirs, files in os.walk(dest_dir):
            for fn in files:
                if fn == zip_filename:
                    continue

                abspath = os.path.join(root, fn)
                relpath = abspath[len(dest_dir) + len(os.sep):]
                relpath = os.path.join('bin', relpath)
                zip.write(abspath, relpath)

        zip.close()

        # clean up
        cleanup([os.path.join(self.dest_dir, 'exe')])

if __name__ == '__main__':
    build = Build(project)
    build.run()
