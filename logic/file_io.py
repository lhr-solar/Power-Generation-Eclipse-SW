from PySide6.QtCore import QObject, Slot
import os

class file_io(QObject):
    def __init__(self):
        super().__init__()
    
    @Slot(str, str)
    def write_file(self, filePath, fileData):
        try:
            with open(filePath, "w") as f:
                f.write(fileData)
            return True
        except Exception as e:
            print(e)
            return False
    
    @Slot(str)
    def read_file(self, filePath):
        try:
            with open(filePath, "r") as f:
                return f.read()
        except Exception as e:
            print(e)
            return "File error"