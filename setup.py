#!/usr/bin/env python

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.
from cx_Freeze import setup, Executable
import matplotlib

# Local modules.

# Globals and constants variables.

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"excludes": ["Tkinter", "wx", "scipy", 'PIL'],
                     "includes": ['encodings.ascii']}

setup(name="fsaecostreport",
      version="0.5.2",
      url='http://fsae.mcgill.ca',
      description="Generator of the FSAE Cost Report",
      author="Philippe T. Pinard",
      author_email="philippe.pinard@gmail.com",
      license="Private",
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Education',
                   'License :: Other/Proprietary License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'],

      packages=['fsaecostreport'],
      package_dir={'fsaecostreport': 'src/fsaecostreport'},

      options={"build_exe": build_exe_options},
      executables=[Executable("src/fsaecostreport/app.py")]
)

