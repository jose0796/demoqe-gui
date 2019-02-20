
import sys 
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "DemoQe Project"
        self.top = 100
        self.left = 50
        self.width = 680 
        self.height = 500
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.InitWindow()
        

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())