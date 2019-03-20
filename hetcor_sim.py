import scripts.test as test
test.working()

""" Cleans Mercury data 
Cleans and references .magres output
Plots 2D NMR spectra with data to visulise correlation between nuclei via dipolar coupling
On hover displays atom labels for correlated nuclei
"""

import scripts.clean_contacts as clean

csv_input = './test_data/contacts_inter.csv' # define path to contacts.csv
csv_output = './test_data/clean_contacts_inter.csv' # where to save file

array = clean.open_csv(csv_input)
del array[0]
print(array)
clean.write_clean_array(array, csv_output)
