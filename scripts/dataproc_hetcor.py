import pandas
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import LogFormatter
from math import log10, floor
import csv
import numpy
import scipy.spatial as spatial
from scipy.constants import pi, hbar

c_shifts_df = pandas.read_csv('../1,2-dichlorobenzene/constrained/C_shifts.csv')
h_shifts_df = pandas.read_csv('../1,2-dichlorobenzene/constrained/H_shifts.csv')
intra_df = pandas.read_csv('../1,2-dichlorobenzene/constrained/clean_contacts_intra.csv')
inter_df = pandas.read_csv('../1,2-dichlorobenzene/constrained/clean_contacts_inter.csv')

def clean(x, string):
    x = x.replace(string, '', 1)
    return x

def round_sf(x, sf=2):
    return(round(x, sf-int(floor(log10(abs(x))))))

def clean_labels(df, string):
    df.label = df.label.apply(clean, args=(string,))
    df = df.set_index('label')
    return df

def get_shift(x):
    if 'C' in x:
        shift = c_shifts_df.loc[x]
    elif 'H' in x:
        shift = h_shifts_df.loc[x]
    return(float(shift))

def calc_dipolar_coupling(x):
    perm = 4e-7*pi
    c_gy = 10.705e-6
    h_gy = 42.576e-6
    b = (perm*c_gy*h_gy*hbar)/(4*pi*(x**3))
    return(float(b))

def fill_df(df):
    df['Atom1_Shift'] = df.Atom1.apply(get_shift)
    df['Atom2_Shift'] = df.Atom2.apply(get_shift)
    df['dipolar_coupling'] = df.Length.apply(calc_dipolar_coupling)
    return df

c_shifts_df = clean_labels(c_shifts_df, '13')
h_shifts_df = clean_labels(h_shifts_df, '1')

intra_df = fill_df(intra_df)
inter_df = fill_df(inter_df)

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
concat_df.to_csv('proc_contacts.csv')
zs = concat_df['dipolar_coupling']

min_, max_ = zs.min(), zs.max()
mid = (min_+max_)/2
min_label, mid_label, max_label = round_sf(min_), round_sf(mid), round_sf(max_)

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

#ax.invert_zaxis() #3d
ax.invert_xaxis()
ax.invert_yaxis()
ax.set_ylabel('H shifts (ppm)')
ax.set_xlabel('C shifts (ppm)')
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
#plt.close(fig)