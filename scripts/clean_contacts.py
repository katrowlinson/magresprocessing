'''
Script to clean Mercury generated .csv contacts data
'''
import csv

csv_path = './1,2-dichlorobenzene/free/inter_contacts.csv' # define path to contacts.csv
csv_save = './1,2-dichlorobenzene/free/clean_contacts_inter.csv' # where to save file
array = []
contact_array = [['Number','Atom1','Atom2','Length']]
bool = []

def open_csv(csv_path):
    with open(csv_path, 'r') as sim_file:
        sim_reader = csv.reader(sim_file, delimiter=',')
        for row in sim_reader:
            array.append(row[0:4])

def check(array):
    for i in array:
        if 'C' in i[1] or 'H' in i[2]:
            bool.append(False)
        else:
            pass
    if all(bool):
        return True
    else:
        return False

def clean(x, string):
    x = x.replace(string, '', 1)
    return x

#needs to change to while loop bc otherwise counter is going up as list is shrinking
def over_max(array):
    for i in array:
        h_int = int(clean(i[1], 'H'))
        c_int = int(clean(i[2], 'C'))
        if h_int < 169 and c_int <109: #change based on shift data available
            contact_array.append(i)
        else:
            pass

# Makes sure atoms are in the correct columns
def correct_columns(array):
    for i in array:
        if 'C' in i[1]:
            c_label = i[1]
            h_label = i[2]
            i[1] = h_label
            i[2] = c_label
        else:
            pass

def write_clean_csv(csv_save, contact_array):
    with open(csv_save, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(contact_array)
    csvFile.close()

def write_clean_array(array):
    if check(array):
        over_max(array)
        write_clean_csv(csv_save, contact_array)
    else:
        correct_columns(array)
        over_max(array)
        write_clean_csv(csv_save, contact_array)

open_csv(csv_path)
del array[0]
write_clean_array(array)
