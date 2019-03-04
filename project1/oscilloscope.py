
#!python 3.x
import sys 
import numpy as np
import math
import random
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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

    def plot(self):
        self.axes.clear()
        data = [random.uniform(0.0,1.0) for i in range(25)]
        self.axes.plot(data)
        self.axes.grid()
        self.axes.set_yticklabels([])
        self.axes.set_xticklabels([])
        self.axes.margins(0)
        
        self.canvas.draw()

""" 
        self.compute_initial_figure()

        
        self.setParent(parent)
def compute_initial_figure(self):
        pass
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self) 

        
    def compute_initial_figure(self):
        pass

class MplLivePlot(MplCanvas):

    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(100)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw() """
    
        

        
        
        



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


        #self.plotFig = QtWidgets.QWidget(self)
        #self.fig = plt.figure()
        #self.axes = self.fig.add_subplot(111)

        self.canvas = MplCanvas(self)
        


        """ self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.move(60,80) """
        
        #l = QtWidgets.QVBoxLayout(self.plotFig)
        #sc = MplLivePlot(self.plotFig, width=5, height=5, dpi=100)
        #l.addWidget(sc)
        #self.plotFig.setFocus() 
        #self.setCentralWidget(self.plotFig)

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
        self.canvas.plot()


    


App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())
