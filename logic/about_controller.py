"""_summary_
@file       about_controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Loads in program information for the about page.

@version    0.0.0
@date       2023-05-11
"""
from PySide6.QtCore import QFile, QObject

def load_about(objs):
    # Load text for about page.
    file = QFile("ui/AboutPage/about.md")
    if file.open(QFile.ReadOnly | QFile.Text):
        text = file.readAll()

        try:
            # Python v3.
            text = str(text, encoding='ascii')
        except TypeError:
            # Python v2.
            text = str(text)

        print(text)
        about_text = objs.findChild(QObject, "about_text")
        about_text.setProperty("text", text)


