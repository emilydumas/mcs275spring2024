# Matplotlib "hello world"
# MCS 275 Spring 2024 Lecture 24
# David Dumas
import numpy as np
import matplotlib.pyplot as plt

# vectors of x and y coords
xv = np.linspace(0, 2 * np.pi, 200)
yv = np.sin(xv)

# Add a plot of y vs x
plt.plot(xv, yv)

# Write the plot to various files
# (format autodetected from name)
plt.savefig("mplhello.pdf")
plt.savefig("mplhello.png")
plt.savefig("mplhello.svg")
