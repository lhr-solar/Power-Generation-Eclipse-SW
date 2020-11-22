"""
Console.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/18/20
Last Modified: 10/18/20

Description: The Console class is a concrete base class that provides a common 
API for derived classes to use. It allows for the generation of textboxes and
buttons in a wrapped widget that can connect to program functions.
"""
# Library Imports.
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
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

    def addButton(self, ID, flavorText, position, size, callback):
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
        self._components[id] = QPushButton(flavorText)
        self._layout.layout.addWidget(
            self._components[id], position[0], position[1], size[0], size[1]
        )

        if callback is not None:
            self._components[id].clicked.connect(callback)
