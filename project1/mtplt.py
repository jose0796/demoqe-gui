import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from com import *
import serial 

##1 example for plotting 
t = [0.1,0.2,0.3,0.4,0.5]
fig= plt.figure()
ax1 = fig.add_subplot(1,1,1)
plt.title('Prueba 1')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()

dataSerial = serial.Serial('/dev/ttyUSB0', baudrate=115200)

def animate(i):
    channel1 = []
    channel2 = []
    data =[]
    data = startReceiving(dataSerial)
    channel1.append(data[0])
    channel2.append(data[1])
    ax1.clear()
    ax1.plot([0.5],channel1)
        
ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
