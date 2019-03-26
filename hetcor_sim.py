""" Cleans Mercury data 
Extracts and references chemical shifts from .magres
Plots 2D NMR spectra with data to visulise correlation between nuclei via dipolar coupling
On hover displays atom labels for correlated nuclei
"""

import scripts.magres_shifts as magres
import scripts.clean_contacts as clean
import scripts.dataproc_hetcor as hetcor

import pandas
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import LogFormatter
from math import log10, floor

def get_shift(x):
    if 'C' in x:
        shift = c_shifts_df.loc[x]
    elif 'H' in x:
        shift = h_shifts_df.loc[x]
    return(float(shift))

def fill_df(df):
    df['Atom1_Shift'] = df.Atom1.apply(get_shift)
    df['Atom2_Shift'] = df.Atom2.apply(get_shift)
    df['dipolar_coupling'] = df.Length.apply(hetcor.calc_dipolar_coupling)
    return df

# CASTEP.magres data cleaning
atoms = magres.load_magres('./test_data/DCA_toluene-out.magres')
data_H = magres.extract_shifts('H', atoms)
data_C = magres.extract_shifts('C', atoms)
magres.write_csv('./test_data/H_shifts.csv', data_H)
magres.write_csv('./test_data/C_shifts.csv', data_C)

# Mercury data cleaning
intra_input = './test_data/contacts_intra.csv' # define path to contacts.csv
intra_output = './test_data/clean_contacts_intra.csv' # where to save file
inter_input = './test_data/contacts_inter.csv' # define path to contacts.csv
inter_output = './test_data/clean_contacts_inter.csv' # where to save file

intra_array = clean.open_csv(intra_input)
inter_array = clean.open_csv(inter_input)
del intra_array[0]
del inter_array[0]

# Writes clean arrays to .csv files for checking and supplementary material
clean.write_clean_array(intra_array, intra_output)
clean.write_clean_array(inter_array, inter_output)

# Reads shift and contacts data into DataFrames
c_shifts_df = pandas.read_csv('./test_data/C_shifts.csv')
h_shifts_df = pandas.read_csv('./test_data/H_shifts.csv')
intra_df = pandas.read_csv('./test_data/clean_contacts_intra.csv')
inter_df = pandas.read_csv('./test_data/clean_contacts_inter.csv')

c_shifts_df = hetcor.clean_labels(c_shifts_df, '13')
h_shifts_df = hetcor.clean_labels(h_shifts_df, '1')

intra_df = fill_df(intra_df)
inter_df = fill_df(inter_df)

# Defining x, y, z for 2D plot
x1 = intra_df['Atom2_Shift']
x1_label = intra_df['Atom2']
y1 = intra_df['Atom1_Shift']
y1_label = intra_df['Atom1']
z1 = intra_df['dipolar_coupling']

x2 = inter_df['Atom2_Shift']
x2_label = inter_df['Atom2']
y2 = inter_df['Atom1_Shift']
y2_label = inter_df['Atom1']
z2 = inter_df['dipolar_coupling']

frames = [intra_df, inter_df]
concat_df = pandas.concat(frames)
#concat_df.to_csv('proc_contacts.csv') # Prints all correlated shift data
zs = concat_df['dipolar_coupling']

# Labels for colorbar
min_, max_ = zs.min(), zs.max()
mid = (min_+max_)/2
min_label, mid_label, max_label = hetcor.round_sf(min_), hetcor.round_sf(mid), hetcor.round_sf(max_)

fig = plt.figure()
plt.rcParams.update({'font.size': 22})
ax = fig.add_subplot(111)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind, sc):
    if sc == 1:
        pos = sc1.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = ', '.join([str(x1_label[n]) + str(y1_label[n]) for n in ind["ind"]])
    elif sc == 2:
        pos = sc2.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = ', '.join([str(x2_label[n]) + str(y2_label[n]) for n in ind["ind"]])
    #print(ind)
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc1.contains(event)
        if cont:
            update_annot(ind, 1)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            cont, ind = sc2.contains(event)
            #print(cont, vis)
            if cont:
                update_annot(ind, 2)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

# Setting up colourmap/scale for dipolar coupling
colormap = plt.cm.plasma_r
norm = matplotlib.colors.LogNorm(min_, max_)
formatter = LogFormatter(10, labelOnlyBase=False)

sc1 = plt.scatter(x1, y1, c=z1, cmap=colormap, norm=norm, marker='x', s=100, label='intra')
#plt.clim(min_, max_)
sc2 = plt.scatter(x2, y2, c=z2, cmap=colormap, norm=norm, marker='v', s=100, label='inter')
#plt.clim(min_, max_)

ax.invert_xaxis()
ax.invert_yaxis()
ax.set_ylabel('H shifts (ppm)')
ax.set_xlabel('C shifts (ppm)')
#set limits for x,y to get consistent and comparable selected regions
#ax.set_xlim((150, 110))
#ax.set_ylim((8, -3))
# ax.set_zlabel('Contact Distance') #3d
# ax.view_init(azim=90, elev=90) #3d
cb = plt.colorbar(format=formatter)
cb.set_ticks([min_, mid, max_])
cb.set_ticklabels([min_label, mid_label, max_label])
cb.set_label('Dipolar Coupling (Hz)')

#cbar = fig.colorbar(plt)
#cbar.set_label('Contact Distance ($\AA$)')
fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()
#fig.savefig('free_guest.png')
#plt.close(fig)"""