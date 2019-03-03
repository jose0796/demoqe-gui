
#!python 3.x
import sys 
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Canvas(FigureCanvas):
    def __init__(self,parent=None, width=5,height=5,dpi=100):
        fig = Figure(figsize=(width,height), dpi=dpi)
        self.axes = fig.add_subplot(1,1,1)


        FigureCanvas.__init__(self,fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
        self.plot()
    def plot(self):
        

        
        
        



class Window(QMainWindow): 
    def __init__(self):
        super().__init__()

        canvas = Canvas(self,width=9,height=8)
        canvas.move(60,60)
        #window config
        self.title = "Demoqe Project"
        self.top = 100
        self.left = 100
        self.width = 1000 
        self.height = 700 
        
        #push button config 
        button = QPushButton("Start", self) 
        button.move(800,300)
        #button.clicked.connect(self.drawGraph)

        #tool tip for push button 
        self.setToolTip("Hello world")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        
        #slider for channel 1
        self.text   = QLabel("Channel 1", self)
        self.text.move(800,75)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(750,100,170,20)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(10)

        #slider for channel 2
        self.text   = QLabel("Channel 2", self)
        self.text.move(800,125)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(750,150,170,20)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(10)

        #position 
        self.text   = QLabel("Position", self)
        self.text.move(800,175)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(750,200,170,20)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(10)


        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title) #show windows title
        self.setGeometry(self.top, self.left, self.width, self.height) #set window geometry
        self.show() #show all above

        


    


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
