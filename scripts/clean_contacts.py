'''
Script to clean Mercury generated .csv contacts data
'''
import csv

contact_array = [['Number','Atom1','Atom2','Length']]
bool = []

# Opens csv file and writes to an array
def open_csv(csv_path):
    with open(csv_path, 'r') as sim_file:
        sim_reader = csv.reader(sim_file, delimiter=',')
        for row in sim_reader:
            array.append(row[0:4])
        return array

# Checks that all C labels are in one column and H shifts in the other
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

# Cleans string x from substring
def clean(x, substring):
    x = x.replace(substring, '', 1)
    return x

# Removes contacts data for atoms not available in shift data
def over_max(array):
    for i in array:
        h_int = int(clean(i[1], 'H'))
        c_int = int(clean(i[2], 'C'))
        if h_int < 353 and c_int <221: #change based on shift data available
            contact_array.append(i)
        else:
            pass

# If labels in incorrect column, switches the labels
def correct_columns(array):
    for i in array:
        if 'C' in i[1]:
            c_label = i[1]
            h_label = i[2]
            i[1] = h_label
            i[2] = c_label
        else:
            pass

# Writes clean contacts data to CSV
def write_clean_csv(csv_save, contact_array):
    with open(csv_save, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(contact_array)
    csvFile.close()

# Writes clean contacts data to an array
def write_clean_array(array, csv_save):
    if check(array):
        over_max(array)
        write_clean_csv(csv_save, contact_array)
    else:
        correct_columns(array)
        over_max(array)
        write_clean_csv(csv_save, contact_array)
