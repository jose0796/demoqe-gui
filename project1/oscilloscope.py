
#!python 3.x
import sys 
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication

class Window(QMainWindow): 
    def __init__(self):
        super().__init__()

        self.title = "Demoqe Project"
        self.top = 100
        self.left = 100
        self.width = 680 
        self.height = 540 
        
        #push button 
        button = QPushButton("Close", self)
        button.move(80,450)
        button.clicked.connect(self.Close)

        self.setToolTip("Hello world")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def Close(self):
        reply = QMessageBox.question(self,"Close Message", "Are you sure to close window?",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes: 
            self.close()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
