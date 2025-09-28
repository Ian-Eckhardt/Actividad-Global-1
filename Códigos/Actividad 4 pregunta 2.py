import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
U, V = np.meshgrid(u, v)

X = np.sin(V) * np.cos(U)
Y = np.sin(V) * np.sin(U)
Z = np.cos(V)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, alpha=0.7)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('x² + y² + z² = 1')
ax.set_box_aspect([1, 1, 1])
plt.show()
