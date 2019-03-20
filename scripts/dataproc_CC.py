'''
Processes contacts data
to generate a visualisation of 
C-C homonuclear correlation
simulation data
'''

import pandas
import matplotlib.pyplot as plt
from matplotlib import cm
import csv
import numpy

# Read data into DataFrame
c_shifts_df = pandas.read_csv('chlorobenzene/C_shifts.csv')
contacts_df = pandas.read_csv('chlorobenzene/cc_contacts.csv')

def clean(x, string):
    x = x.replace(string, '', 1)
    return x

# Cleans labels so DataFrames are compatible
c_shifts_df.label = c_shifts_df.label.apply(clean, args=('13',))
c_shifts_df = c_shifts_df.set_index('label')

# Needed to colour map diagonal peaks
no_shifts = len(c_shifts_df.index)
a = [1.2]*no_shifts

# Retrieve shifts from DataFrame
def get_shift(x):
    if 'C' in x:
        shift = c_shifts_df.loc[x]
        return(float(shift))
    else:
        pass

# New dataframe for plotting
cc_df = contacts_df.filter(['Atom1', 'Atom2', 'Length'], axis=1)

# Get shifts for each Atom
cc_df['Atom1_Shift'] = cc_df.Atom1.apply(get_shift)
cc_df['Atom2_Shift'] = cc_df.Atom2.apply(get_shift)

# Convert to list for easy concatenation
diag_shifts = c_shifts_df['shift'].values.tolist()
Atom1_shifts = cc_df['Atom1_Shift'].values.tolist()
Atom2_shifts = cc_df['Atom2_Shift'].values.tolist()
length = cc_df['Length'].values.tolist()

# Needed so that plot looks like a 2D expt
x = diag_shifts + Atom1_shifts + Atom2_shifts
y = diag_shifts + Atom2_shifts + Atom1_shifts
z = a + length + length

# Plot visualisation
fig = plt.figure()
plt.rcParams.update({'font.size': 22})
ax = fig.add_subplot(111)
p = ax.scatter(x, y, c=z, cmap='viridis', marker='x')

ax.invert_xaxis()
ax.invert_yaxis()
ax.set_ylabel('C shifts (ppm)')
ax.set_xlabel('C shifts (ppm)')

cbar = fig.colorbar(p)
cbar.set_label('Contact Distance ($\AA$)')
plt.show()
