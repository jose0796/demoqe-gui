import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np
import math as mt
from com import *
import serial 

##1 example for plotting 

fig= plt.figure()
ax1 = fig.add_subplot(1,1,1)


def convert(data, max=3, min=0, bitnum=12): 
    data_converted = float(data*(max-min)/(2**12))
    return data_converted


def animate(i):
    channel1 = []
    channel2 = []
    data =[]
    timescale = np.linspace(start=0,stop=1,num=2000,endpoint=True)
    while len(channel1) != len(timescale):
        data = startReceiving(dataSerial)
        channel1.append(convert(data[0]))
        channel2.append(convert(data[1]))
    ax1.clear()
    ax1.plot(timescale,channel1,timescale,channel2)

        
ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
