import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

x = np.linspace(-10,10,500)

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(1, 2)

def fg(x):
    return 1/(2 + np.e**x)

def gf(x):
    return np.log(1 + np.e**(1/(1 + np.e**x)))


ax = fig.add_subplot(gs[0, 0])
ax.set_title("f◦g")
ax.plot(x, fg(x), color='red')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[0, 1])
ax.set_title("g◦f")
ax.plot(x, gf(x), color='crimson')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

fig.align_labels()
plt.show()
