""" Cleans Mercury data 
Extracts and references chemical shifts from .magres
Plots 2D NMR spectra with data to visulise correlation between nuclei via dipolar coupling
On hover displays atom labels for correlated nuclei
"""

import scripts.clean_contacts as clean

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
