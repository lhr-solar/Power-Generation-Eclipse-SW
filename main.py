"""_summary_
@file       main.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for loading the application.
@version    0.4.0
@date       2023-05-13
"""
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from logic.about_controller import load_about


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)

    objs = engine.rootObjects()[0]
    load_about(objs)

    sys.exit(app.exec())
