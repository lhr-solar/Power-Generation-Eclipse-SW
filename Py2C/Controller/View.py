"""
View.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/17/20
Last Modified: 11/24/20

Description: The View class is a concrete base class that provides a common API
for derived classes to use. It manages the widgets within each tab during their
lifetimes. A View roughly corresponds to a tab in the PVSimulator.
"""
# Library Imports.
from PyQt5.QtGui import QColor, QPalette


# Custom Imports.


class View:
    """
    The View class is a concrete base class that provides a common API for
    derived classes to use. It manages the widgets within each tab during their
    lifetimes. A View roughly corresponds to a tab in the PVSimulator.
    """

    # Some internal color palettes.
    _lightGray = QColor(76, 76, 76, 255)
    _mediumGray = QColor(64, 64, 64, 255)
    _darkGray = QColor(51, 51, 51, 255)
    _red = QColor(255, 0, 0, 255)
    _green = QColor(0, 255, 0, 255)

    # Timing constants.
    _SECOND = 1000  # in milliseconds.

    def __init__(self, dataController=None, framerate=60):
        """
        Initializes a view object for displaying data.

        Parameters
        ----------
        dataController: Dictionary
            reference to the DataController object which manages the program
            simulation pipeline.
        framerate: int
            Number of updates per second for realtime graphing and graphics.
        """
        self._framerate = framerate
        self._layout = None

        # The datastoreParent is a reference to the overarching DataController,
        # which exposes its API to user Views.
        self._datastoreParent = dataController

        # The datastore child is a reference to a local managed datastore, which
        # is of a different format as the parent.
        self._datastore = None

    def getLayout(self):
        """
        Returns a reference to the View layout.

        Returns
        -------
        layout of the View.
        """
        return self._layout

    def getDatastore(self):
        """
        Returns a reference to the internal data representation.

        Returns
        -------
        Data store of the view. Could be any type.
        """
        return self._datastore
