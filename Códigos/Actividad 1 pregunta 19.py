import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

x = np.linspace(-10,10,500)
x1 = np.linspace(-1,1,100)[1:-1]
fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(3, 3)

def PB(x):
    if x < 0:
        fx = 0
    else:
        fx = 1
    return fx

def ReLU(x):
    if x<=0:
        fx = 0
    else:
        fx = x
    return fx

def PReLU(x):
    if x < 0:
        fx = 7*x
    else:
        fx = x
    return fx

def ELU(x):
    if x < 0:
        fx = 5*(np.exp(x) - 1)
    else:
        fx = x
    return fx

ax = fig.add_subplot(gs[0, 0])
ax.set_title("Identidad")
ax.plot(x, x, color='red')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[0, 1])
ax.set_title("Paso Binario")
ax.plot(x,[PB(i) for i in x], color='orangered')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[0, 2])
ax.set_title("Sigmoide")
ax.plot(x, (1/(1+ np.exp(-x))), color='gold')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[1, 0])
ax.set_title("Tangente hiperbólica")
ax.plot(x, np.tanh(x), color='orange')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[1, 1])
ax.set_title("Arcotangente hiperbólica")
ax.plot(x1, np.arctanh(x1), color='lime')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[1, 2])
ax.set_title("ReLU")
ax.plot(x,[ReLU(i) for i in x], color='turquoise')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[2, 0])
ax.set_title("PReLU")
ax.plot(x,[PReLU(i) for i in x], color='dodgerblue')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[2, 1])
ax.set_title("ELU")
ax.plot(x,[ELU(i) for i in x], color='blue')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()

ax = fig.add_subplot(gs[2, 2])
ax.set_title("Softplus")
ax.plot(x, (np.log(1 + np.exp(x))), color='purple')
ax.set_ylabel('$f(x)$')
ax.set_xlabel('$x$')
ax.grid()


fig.align_labels()
plt.show()
