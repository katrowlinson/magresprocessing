from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import csv
import numpy

x, y, z = [], [], []
# read in excel data
with open('mxylene_2D_sim.csv', 'r') as sim_file:
    sim_reader = csv.reader(sim_file, delimiter=',')
    for row in sim_reader:
        x.append(float(row[0]))
        y.append(float(row[1]))
        z.append(float(row[2]))
# x = C shifts, y = H shifts, z = contact distance in Angstrom

#Z needs to be x by y with z along diagonal and all othe values 0

#Z = numpy.zeros((len(x), len(y)))
#print(Z.shape)
#numpy.fill_diagonal(Z, z)

fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#surf = ax.plot_surface(x, y, Z, cmap='viridis')

ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

plt.show()
