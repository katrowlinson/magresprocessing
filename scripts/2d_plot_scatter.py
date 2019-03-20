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
    print(z)
# x = C shifts, y = H shifts, z = contact distance in Angstrom

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=z, cmap='viridis')

ax.invert_zaxis()
ax.invert_yaxis()
ax.set_xlabel('H shifts')
#ax.set_xlim(-40, 40)
ax.set_ylabel('C shifts')
#ax.set_ylim(-40, 40)
ax.set_zlabel('Contact Distance')
#ax.set_zlim(-100, 100)

ax.view_init(azim=0, elev=90)
plt.show()
