#!python 3.x
import os
import sys 
import serial 
from com import *
import numpy as np
import math
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def showScale(scl):
    if scl == 0:
        return 0.3
    elif scl == 1:
        return 1
    elif scl == 2:
        return 3

def scaleYAxis(scl): 
    if scl== 0:
        return 1
    elif scl == 1:
        return 3/10
    elif scl == 2:
        return 1/10

def scaleTimeAxis(time=2):
    return 2*(10**(time+1))

def timeScaleFactor(time=2):
    return 10**(time-2)

def showDivScales(self,scale2: str,scale1: str, xpos) -> None:
    self.axes.text(xpos,0.5,"channel 1: %.1f" % scale1)
    self.axes.text(xpos,0.3,"channel 2: %.1f" % scale2)

class MplCanvas(FigureCanvas):
    
    def __init__(self, parent=None, width=1, height=1, dpi=100):
        self.fig = plt.figure()
        self.fig.subplots_adjust(left=0.1,right=0.9,top=0.9,bottom=0.1)
        FigureCanvas.__init__(self, self.fig)
        
        self.axes = self.fig.add_subplot(111)
        self.axes.set_yticklabels([])
        self.axes.set_xticklabels([])
        self.axes.grid()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.canvas.move(60,80)
        self.channel1 = []
        self.channel2 = []

        self.timescale = np.linspace(start=0,stop=1,num=1000,endpoint=True)
        self.xticks = np.linspace(0,1,10)
        self.yticks = np.linspace(0,3,10)

        self.dataSerial = serial.Serial('/dev/ttyUSB1', baudrate=115200)
        self.axes.xaxis.set_ticks(self.xticks)
        self.axes.yaxis.set_ticks(self.yticks)


    def plot(self,ch1=0, ch2=0,time=2):
        def _plot():
            self.update_figure(ch1,ch2,time)
        return _plot

    def update_figure(self,ch1=0, ch2=0, time=2):
        self.axes.clear()
        data = []
        i = 0
        if len(self.channel1) != len(self.timescale):
            while len(self.channel1) != len(self.timescale):
                data = startReceiving(self.dataSerial)
                self.channel1.append(scaleYAxis(ch1)*convert(data[0]))
                self.channel2.append(scaleYAxis(ch2)*convert(data[1]))
        else: 
            while i < 300:
                data = startReceiving(self.dataSerial)
                print(self.channel1.pop(0))
                self.channel2.pop(0)
                self.channel1.append(scaleYAxis(ch1)*convert(data[0]))
                self.channel2.append(scaleYAxis(ch2)*convert(data[1]))
                i = i + 1


        ts = scaleTimeAxis(time)
        xlim = [timeScaleFactor(time)*i for i in [0.0, 1.0]]
        self.xticks = np.linspace(0,xlim[1],10)
        

        self.axes.plot(self.timescale[0:ts],self.channel1[0:ts], self.channel2[0:ts])
        showDivScales(self,showScale(ch2),showScale(ch1),0.7*xlim[1])
        self.axes.xaxis.set_ticks(self.xticks)
        self.axes.yaxis.set_ticks(self.yticks)
        self.axes.set_xlim(xlim)
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

        self.timer = None

        #window config
        self.title = "Demoqe Project"
        self.top = 100
        self.left = 100
        self.width = 1000 
        self.height = 600 
        
        #push button config 
        button = QPushButton("Start", self) 
        button.move(790,300)
        button.clicked.connect(self.__plot(0))

        #tool tip for push button 
        # self.setToolTip("Hello world")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        
        #slider for channel 1
        self.text = QLabel("Channel 1", self)
        self.text.move(800,75)

        self.channel1 = QSlider(Qt.Horizontal, self)
        self.channel1.setGeometry(750,100,170,20)
        self.channel1.setMinimum(0)
        self.channel1.setMaximum(2)
        self.channel1.setTickPosition(QSlider.TicksAbove)
        self.channel1.setTickInterval(1)
        self.channel1.valueChanged.connect(self.channel1ChangedValue)

        #slider for channel 2
        self.text = QLabel("Channel 2", self)
        self.text.move(800,125)

        self.channel2 = QSlider(Qt.Horizontal, self)
        self.channel2.setGeometry(750,150,170,20)
        self.channel2.setMinimum(0)
        self.channel2.setMaximum(2)
        self.channel2.setTickPosition(QSlider.TicksAbove)
        self.channel2.setTickInterval(1)
        self.channel2.valueChanged.connect(self.channel2ChangedValue)

        #position 
        self.text = QLabel("Position", self)
        self.text.move(800,175)

        self.position = QSlider(Qt.Horizontal, self)
        self.position.setGeometry(750,200,170,20)
        self.position.setMinimum(0)
        self.position.setMaximum(2)
        self.position.setTickPosition(QSlider.TicksAbove)
        self.position.setTickInterval(1)
        self.position.valueChanged.connect(self.positionChanged)

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title) #show windows title
        self.setGeometry(self.top, self.left, self.width, self.height) #set window geometry
        self.show() #show all above

    def fileQuit(self): 
        self.close()
        
    def channel1ChangedValue(self):
        self.plot(self.channel1.value(), self.channel2.value())    

    def channel2ChangedValue(self):
        self.plot(self.channel1.value(), self.channel2.value()) 

    def positionChanged(self):
        self.plot(self.channel1.value(),self.channel2.value(),self.position.value())

    def __plot(self,option=1):
        def ___plot():
            if option == 0:
                self.plot()

        return ___plot


    def plot(self,opt1=0, opt2=0,opt3=2):
        ''' plot some random stuff '''
        if self.timer: 
            self.timer.stop()
            self.timer.deleteLater()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.canvas.plot(opt1,opt2,opt3))
        self.timer.start(116)

        


    


App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())
