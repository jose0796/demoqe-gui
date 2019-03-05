import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
from matplotlib import style 

fig = plt.figure()
ax = fig.add_subplot(1,1,1)


def animate(i):
    graph_data = open('sample.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line)> 1:
            x, y = line.split(',')
            print("x: %d, y: %d" % (int(x),int(y)))
            xs.append(x)
            ys.append(y)

    ax.clear()
    ax.plot(xs,ys)

ani = animation.FuncAnimation(fig,animate,interval=1000)
plt.show()