"""
Console.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 11/24/20

Description: The Console class is a concrete base class that provides a common 
API for derived classes to use. It allows for the generation of textboxes and
buttons in a wrapped widget that can connect to program functions.
"""
# Library Imports.
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QComboBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# Custom Imports.
from ArraySimulation.Controller.View import View


class Console(View):
    """
    The Console class is a concrete base class that provides a common
    API for derived classes to use. It allows for the generation of textboxes
    and buttons in a wrapped widget that can connect to program functions.
    """

    def __init__(self):
        self._components = {}
        layoutWidget = QWidget()
        layoutWidget.layout = QGridLayout()
        layoutWidget.setLayout(layoutWidget.layout)

        self._layout = layoutWidget

    def addButton(self, ID, flavorText, position, size, callback=None):
        """
        Adds a button to the layout with a bindable callback.

        Parameters
        ----------
        ID: String
            Unique identifier for the button.
        flavorText: String
            Text to be displayed on the button.
        position: (int, int)
            Location of the button in grid coordinates.
        size: (int, int)
            Size of the button in grid coordinates.
        callback: function reference
            Function that will trigger when pressed.
        """
        self._components[ID] = QPushButton(flavorText)
        self._layout.layout.addWidget(
            self._components[ID], position[0], position[1], size[0], size[1]
        )

        if callback is not None:
            self._components[ID].clicked.connect(callback)

    def addTextbox(self, ID, position, size, hint=""):
        """
        Adds a textbox to the layout.

        Parameters
        ----------
        ID: String
            Unique identifier for the button.
        position: (int, int)
            Location of the button in grid coordinates.
        size: (int, int)
            Size of the button in grid coordinates.
        hint: String
            Optional text to be displayed on an empty textbox.
        """
        self._components[ID] = QLineEdit()
        self._components[ID].setPlaceholderText(hint)
        self._layout.layout.addWidget(
            self._components[ID], position[0], position[1], size[0], size[1]
        )

    def addLabel(self, ID, position, size, defaultText=""):
        """
        Adds a label to the layout.

        Parameters
        ----------
        ID: String
            Unique identifier for the button.
        position: (int, int)
            Location of the button in grid coordinates.
        size: (int, int)
            Size of the button in grid coordinates.
        defaultText: String
            Optional starter text to display on the label.
        """
        self._components[ID] = QLabel(defaultText)
        self._layout.layout.addWidget(
            self._components[ID], position[0], position[1], size[0], size[1]
        )

    def addComboBox(self, ID, position, size, options, callback=None):
        """
        Adds a combo box to the layout. The combo box can have a callback
        attached to do something when the user clicks an item.

        Parameters
        ----------
        ID: String
            Unique identifier for the button.
        position: (int, int)
            Location of the button in grid coordinates.
        size: (int, int)
            Size of the button in grid coordinates.
        options: [String]
            A list of strings representing each item in the combo box.
        """
        self._components[ID] = QComboBox()
        self._components[ID].addItems(options)
        self._layout.layout.addWidget(
            self._components[ID], position[0], position[1], size[0], size[1]
        )

        if callback is not None:
            self._components[ID].currentIndexChanged.connect(callback)

    def hideConsoleWidgets(self, IDs=[]):
        """
        Hides a list of widgets from the console.

        Parameters
        ----------
        IDs: [String]
            A list of IDs of widgets that should be hidden.
        """
        for ID in IDs:
            component = self._components.get(ID)
            if component is not None:
                component.hide()

    def showConsoleWidgets(self, IDs=[]):
        """
        Shows a list of widgets from the console.

        Parameters
        ----------
        IDs: [String]
            A list of IDs of widgets that should be shown.
            Assumes they were created prior.
        """
        for ID in IDs:
            component = self._components.get(ID)
            if component is not None:
                component.show()

    def getReference(self, ID):
        """
        Returns the widget, if any, of the console corresponding to the correct
        ID.

        Parameters
        ----------
        ID: String
            ID reference to the widget.

        Returns
        -------
        Reference to the widget, or None.
        """
        return self._components.get(ID)
