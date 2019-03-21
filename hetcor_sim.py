""" Cleans Mercury data 
Extracts and references chemical shifts from .magres
Plots 2D NMR spectra with data to visulise correlation between nuclei via dipolar coupling
On hover displays atom labels for correlated nuclei
"""

import scripts.magres_shifts as magres
import scripts.clean_contacts as clean
import scripts.dataproc_hetcor as hetcor
import pandas

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
contacts_intra_df = pandas.read_csv('./test_data/clean_contacts_intra.csv')
contacts_inter_df = pandas.read_csv('./test_data/clean_contacts_inter.csv')