import numpy as np
import matplotlib.pyplot as plt

xv = np.linspace(0, 2 * np.pi, 200)
yv = np.sin(xv)

plt.plot(xv, yv)

plt.savefig("mplhello.pdf")
plt.savefig("mplhello.png")
plt.savefig("mplhello.svg")
