#!python 3.x
import sys 
import serial 
from com import *
import numpy as np
import math
import random
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class MplCanvas(FigureCanvas):
    
    def __init__(self, parent=None, width=1, height=1, dpi=100):
        self.fig = plt.figure()
        FigureCanvas.__init__(self, self.fig)
        #Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_yticklabels([])
        self.axes.set_xticklabels([])
        self.axes.grid()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.canvas.move(60,80)
        self.dataSerial = serial.Serial('/dev/ttyUSB0', baudrate=115200)

    def plot(self):
        self.update_figure()
        

    def update_figure(self):
        self.axes.clear()
        channel1 = []
        channel2 = []
        data =[]
        timescale = np.linspace(start=0,stop=1,num=2000,endpoint=True)
        while len(channel1) != len(timescale):
            data = startReceiving(self.dataSerial)
            channel1.append(convert(data[0]))
            channel2.append(convert(data[1]))
        self.axes.plot(timescale,channel1)
        self.axes.set_xlim([0.0, 1.0])
        self.axes.set_ylim([0.0, 3.0])
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
        self.axes.grid()
        self.canvas.draw()
        

class Window(QMainWindow): 
    def __init__(self):
        super().__init__()

        #Status bar 
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.canvas = MplCanvas(self)

        #window config
        self.title = "Demoqe Project"
        self.top = 100
        self.left = 100
        self.width = 1000 
        self.height = 700 
        
        #push button config 
        button = QPushButton("Start", self) 
        button.move(800,300)
        button.clicked.connect(self.plot)

        #tool tip for push button 
        self.setToolTip("Hello world")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        
        #slider for channel 1
        self.text   = QLabel("Channel 1", self)
        self.text.move(800,75)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(750,100,170,20)
        self.slider.setMinimum(0)
        self.slider.setMaximum(2)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(1)

        #slider for channel 2
        self.text   = QLabel("Channel 2", self)
        self.text.move(800,125)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(750,150,170,20)
        self.slider.setMinimum(0)
        self.slider.setMaximum(2)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(1)

        #position 
        self.text   = QLabel("Position", self)
        self.text.move(800,175)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(750,200,170,20)
        self.slider.setMinimum(0)
        self.slider.setMaximum(2)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(1)

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title) #show windows title
        self.setGeometry(self.top, self.left, self.width, self.height) #set window geometry
        self.show() #show all above

    def fileQuit(self): 
        self.close()
    
    def plot(self):
        ''' plot some random stuff '''
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.canvas.plot)
        timer.start(1)
        


    


App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())
