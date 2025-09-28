import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

x = np.linspace(-5,5,500)

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(1, 2)

def Cuadrado(x):
    return x**2

def Seno(x):
    return np.sin(x)


ax = fig.add_subplot(gs[0, 0])
ax.set_title("No función")
ax.plot(Cuadrado(x),x, color='red')
plt.axvline(x=15, color='purple')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[0, 1])
ax.set_title("Función")
ax.plot(x,Seno(x), color='coral')
plt.axvline(x=2, color='purple')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

fig.align_labels()
plt.show()
