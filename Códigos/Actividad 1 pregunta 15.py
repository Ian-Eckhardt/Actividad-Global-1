import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

x = np.linspace(-10,10,500)

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(1, 2)

def Cuadrado(x):
    return x**2

def Cubo(x):
    return x**3


ax = fig.add_subplot(gs[0, 0])
ax.set_title("No invertible")
ax.plot(x,Cuadrado(x), color='red')
ax.axhline(y=50, color='b')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[0, 1])
ax.set_title("Invertible")
ax.plot(x,Cubo(x), color='coral')
ax.axhline(y=-450, color='b')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

fig.align_labels()
plt.show()
