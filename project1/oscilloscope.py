#!python 3.x
###############################################
## Author: Jose Moran
## Github: jose0796
## email : jmoran071996@gmail.com
###############################################

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


#Calculate scaling to show on annotation
def showScale(scl):
    if scl == 0:
        return 0.3
    elif scl == 1:
        return 1
    elif scl == 2:
        return 3

#Calculate y's axis scaling factor 
def scaleYAxis(scl): 
    if scl== 0:
        return 1
    elif scl == 1:
        return 3/10
    elif scl == 2:
        return 1/10

#Calculate proper window for slicing arrays 
#and plot correctly. 
def scaleTimeAxis(time=2):
    return 2*(10**(time+1))

#Calculate x's scaling factor 
def timeScaleFactor(time=2):
    return 10**(time-2)

#show scales on graphs as an annotation
def showDivScales(self,scale2: str,scale1: str, xpos) -> None:
    self.axes.text(xpos,0.5,"channel 1: %.1f" % scale1)
    self.axes.text(xpos,0.3,"channel 2: %.1f" % scale2)

class MplCanvas(FigureCanvas):
    #this is a canvas which inherits from FigureCanvas
    #below is the initial state of the object 

    def __init__(self, parent=None, width=1, height=1, dpi=100):

        self.fig = plt.figure() #create a new figure 
        #adjust margins. This is not properly working 
        self.fig.subplots_adjust(left=0.1,right=0.9,top=0.9,bottom=0.1)
        #initialize parent class 
        FigureCanvas.__init__(self, self.fig)
        
        #create new subplot 
        self.axes = self.fig.add_subplot(111)
        #hide x's and y's labels 
        self.axes.set_yticklabels([])
        self.axes.set_xticklabels([])
        ########################
        # add a grid as require for the project 
        self.axes.grid()
        #new canvas object to embed the figure of matplotlib in PyQt5
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent) #really important to do this for the gui to show image
        self.canvas.move(60,80) #set horizontal and vertical position of canvas 

        #these are empty arrays for channel data 
        self.channelA1 = []
        self.channelA2 = []
        self.channelD1 = []
        self.channelD2 = []

        #timescale is set invariable 
        self.timescale = np.linspace(start=0,stop=1,num=2000,endpoint=True)
        #set the number of intervals in the specify range
        self.xticks = np.linspace(0,1,10) #these both are based on project requirements
        self.yticks = np.linspace(0,3,10)
        self.axes.xaxis.set_ticks(self.xticks) #set them both at the graph
        self.axes.yaxis.set_ticks(self.yticks)

        #open serial port for serial communication with DEM0QE
        self.dataSerial = serial.Serial('/dev/ttyUSB1', baudrate=115200)

        
    #based function for calling update_figure with parameters given 
    #by the gui 
    def plot(self,ch1=0, ch2=0,time=2):
        def _plot():
            self.update_figure(ch1,ch2,time)
        return _plot
    #this function is the graphing and update function of the system.
    #this receive data from the proper sliders and makes corrections to
    #the graph in order to correctly show the information received by 
    #the microprocessor 

    def update_figure(self,ch1=0, ch2=0, time=2):
        #clear graph in order to create a new one
        self.axes.clear()
        #empty array to receive data from DEM0QE
        data = []
        #dummy iterator
        i = 0
        #if channel1 or channel2 arrays are empty fill them to the maximun requiered
        if len(self.channelA1) != len(self.timescale):
            while len(self.channelA1) != len(self.timescale):
                #receive data from DEM0QE
                data = startReceiving(self.dataSerial)
                #convert data from binary to proper voltage value and scale 
                #to adjust view scale in gui. Then, append to both of analog channels.
                #For digital channels just receive and append, 1-> 3V and 0 -> 0V. 
                self.channelA1.append(scaleYAxis(ch1)*convert(data[0]))
                self.channelA2.append(scaleYAxis(ch2)*convert(data[1]))
        else: 
            #if array already full then refresh partly in order to  
            #enhance rendering performance and not get too stuck on
            #data reception 
            while i < 300:
                #receive data from DEM0QE
                data = startReceiving(self.dataSerial)
                #pop data from first element in order to add new ones
                self.channelA1.pop(0)
                self.channelA2.pop(0)
                #as before, process and convert data to proper value 
                #and append to both arrays for plotting 
                self.channelA1.append(scaleYAxis(ch1)*convert(data[0]))
                self.channelA2.append(scaleYAxis(ch2)*convert(data[1]))
                i = i + 1

        #calculate proper time per division scale 
        ts = scaleTimeAxis(time)
        #set new x limit in case of new time scale 
        xlim = [timeScaleFactor(time)*i for i in [0.0, 1.0]]
        #new xticks for new time scale
        self.xticks = np.linspace(0,xlim[1],10)
        
        #plot graph. Slicing is done in order to adjust x's axis. 
        self.axes.plot(self.timescale[0:ts],self.channelA1[0:ts], self.channelA2[0:ts])
        #this commands adds an annotation to show scale of every channel
        showDivScales(self,showScale(ch2),showScale(ch1),0.7*xlim[1])
        #set ticks interval for axis
        self.axes.xaxis.set_ticks(self.xticks)
        self.axes.yaxis.set_ticks(self.yticks)
        self.axes.set_xlim(xlim)
        self.axes.set_ylim([0.0, 3.0])
        #hide ticks labels 
        self.axes.set_xticklabels([])
        self.axes.set_yticklabels([])
        #show grid requiered 
        self.axes.grid()
        #draw everything to the canvas 
        self.canvas.draw()
        
        

class Window(QMainWindow): 
    def __init__(self):
        super().__init__()

        #Status bar 
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)
        #Help option
        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        #create canvas object 
        self.canvas = MplCanvas(self)

        #timer configuration for refreshing graph
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

        #time per division slider 
        self.text = QLabel("Time Division", self)
        self.text.move(800,175)

        self.time = QSlider(Qt.Horizontal, self)
        self.time.setGeometry(750,200,170,20)
        self.time.setMinimum(0)
        self.time.setMaximum(2)
        self.time.setTickPosition(QSlider.TicksAbove)
        self.time.setTickInterval(1)
        self.time.valueChanged.connect(self.timeChanged)

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title) #show windows title
        self.setGeometry(self.top, self.left, self.width, self.height) #set window geometry
        self.show() #show all above

    def fileQuit(self): 
        self.close() #exit application
        
    def channel1ChangedValue(self):
        #function for channel 1 slider changed in value
        self.plot(self.channel1.value(), self.channel2.value())    

    def channel2ChangedValue(self):
        #function for channel 2 slider changed in value
        self.plot(self.channel1.value(), self.channel2.value()) 

    def timeChanged(self):
        #function for time division slider changed in value
        self.plot(self.channel1.value(),self.channel2.value(),self.position.value())

    def __plot(self,option=1):
        def ___plot():
            if option == 0:
                self.plot()

        return ___plot


    def plot(self,ch1=0, ch2=0, time=2):
        
        #if timer is running stop and restart a new one
        if self.timer: 
            self.timer.stop()
            self.timer.deleteLater()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.canvas.plot(ch1,ch2,ch3))
        self.timer.start(2.5) 
        #as 60Hz, indicates a 1/60 s or 16.6ms refreshing time. 
        #As we are partly refresshing the graph. Only 15% 
        #we shall refresh every 2.5ms 


        


    
#Run GUI 

App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())
