import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

x = np.linspace(0.01,10,500)

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(1, 2)

def A(x):
    return 0.3**x

def B(x):
    return np.lib.scimath.logn(0.3, x)


ax = fig.add_subplot(gs[0, 0])
ax.set_title("Función")
ax.plot(x,A(x), color='red')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[0, 1])
ax.set_title("Inversa")
ax.plot(x,B(x), color='coral')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

fig.align_labels()
plt.show()
