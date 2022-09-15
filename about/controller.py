"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      About Controller. 
@version    3.0.0
@date       2022-09-14
"""

from textwrap import dedent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class AboutController:
    def __init__(self):
        self.data = self.Data(self)
        self.ui = self.UI(self)

        # Update the UI with relevant setup data.
        self.ui.set_text(
            dedent(
                """
        # Eclipse

        Eclipse is a multifunctional application whose purpose is primarily to
        characterize the University of Texas at Austin's Longhorn Racing Solar's
        power generation system. It allows users to talk to the IV Curve Tracer
        PCB, characterize photovoltaics, compare them against a baseline, and
        create and simulate photovoltaic systems across a set of environmental
        conditions.

        ---
        ## What's New (Doc)

        `Version 3.0.0`

        - The third major revision of the MPPT Simulator. This version
          integrates two more "modules" to the application:
          - A PV Capture application that deals with experimental data and
            characterization
          - A Sim Designer that provides a GUI to generate simulation
            configuration files that was previously performed by pre-written
            JSON files.
        - Views for the original module, the Power Gen Sim, now adds capability
          to model and visualize specific parts of the PV, instead of the whole
          thing.
        - The code backend has been reworked, cleaning up the controllers and
          using inner python classes to manage GUI elements.
        - New file formats for characterization, profiling, and simulation have
          been introduced.
        - More user facing knobs have been added so different parameters can be
          adjusted.
        
        ---
        ## Credits

        The main author of this revision is Matthew Yu (matthewjkyu@gmail.com).
        The assistant author is Roy Moore.

        Also credits to the following members of LHR Solar who have contributed
        previously to MPPT algorithm components:
        - Afnan Mir
        - Gary Hallock

        ---
        ## Copyright


        Copyright (C) 2022 by Matthew Yu

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.

        Dependencies:
        - black (MIT)
        - PyQt6 (GPL v3)
        - screeninfo (MIT)
        """
            )
        )

    def get_data(self):
        return [self.data, "About"]

    def get_ui(self):
        return [self.ui, "About"]

    class Data:
        def __init__(self, parent):
            self.parent = parent

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            self.text_edit = QTextEdit()
            layout = QVBoxLayout()
            layout.addWidget(self.text_edit)

            self.setLayout(layout)

        def set_text(self, text):
            self.text_edit.setMarkdown(text)
