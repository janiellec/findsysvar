import os
import csv

# Double checks if a file name exists
# If all do, returns nothing
#   else, return a list from the .csv that don't exist

#r'\\hqdata02\calaunjr\System Variable List\v833155'
#r'C:\Users\calaunjr\Desktop\System Variable List\v833155'
#pot_files.csv
#
#r'C:\Users\calaunjr\Desktop\TEST
#test.csv

def setup_files(set_name, directory):
    suf = ".kl"
    setcsv = open(set_name + '.csv', "w")
    setup_file = csv.writer(setcsv)
    string = ('C:\\Users\\calaunjr\\Desktop\\Finding System Variable\\System Variable List\\', directory)
    dire = "".join(string)
    for root, dir, files in os.walk(dire):
        for all in files:
            all = all.replace(suf, "")
            setup_file.writerow([all])

## Try this one!!!!
def file_exist(list, setup):
    with open(list, 'r') as t1, open(setup, 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()
    filestatus = False                                  #nothing in not_exist file
    with open('not_exist.csv', 'w') as outfile:
        for line in fileone:
            if line not in filetwo:
                outfile.write(line)
                filestatus = True                       # at least 1 thing in not_exist file
    if filestatus is False:                         # less than 1 thing in not_exist file
        print('All files correct')
        os.remove("not_exist.csv")
                

#### Main ########

if __name__ is '__main__':
    directory = input('Enter setup file directory under System Variable List: ')
    setname = input('Enter desired file list name (no file ext.): ')
    setup_files(setname, directory)
    comparefile = input('Enter csv file to check (no file ext.): ')
    file_exist(comparefile + '.csv', setname + '.csv')
