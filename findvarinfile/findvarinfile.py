
import re
import os
import csv

# Finds variables in files provided using
#       this format: $__something__<whatever demarcation used the file>
# Does not take variables in error or comment functions (often duplicates & 
#       and does not fit format). Removes whitespaces if those exist
# Manual post-processing necessary to find special cases such as:
#       1. '$__something__[' + variable + '].$__somelse__[' + number + ']
#                         ^ premature       ^ searches for this second
#                         termination       $ indication and demarcation
#           - need to double check that every $....[ is closed off or
#               includes the second part connected to it as opposed to separate
#       2. '$__something__' + gunnumber + '[' + number + '].$__someelse__'
#                         ^ premature termination
#           - need to include gun number; not sure how many guns there are

# Helper function: reads into a list and sees if it finds object
# Returns bool of whether list of lines has character
def search(list, character):
    for line in list:
        if character in line:
            return True
    return False

# Finds files that might have system variables
def sysfiles(directory):
    #path = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/System Variable List/' + directory
    path = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/findvarinfile/' + directory
    #path = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/BodyShop/' + directory
    #path = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/' + directory
    print(path)
    list = []
    countfiles, total = 0, 0
    for root, dir, files in os.walk(path):
        for file in files:
            with open(path + '/' + file, 'r', encoding='latin-1') as one:
                linelist = one.readlines()
                total += 1
                if search(linelist, '$'):
                    list.append(file)
                    countfiles += 1
                    continue
    print("Found " + str(countfiles) + " files with potential system variables out of " + str(total) + " files in " + directory)
    return list

# Determines what demarcation marks the end of a sysvar given the file type
def fileext(name):
    ext = name[name.find('.'):]
    if ext == ".kl":
        return "\'"
    elif ext == ".ls":
        return "\s|\="
    elif ext == ".xml" or ext == ".stm":
        return "\""
    elif ext == ".kls":
        return "\s|\'"
    else:
        return "\s"

# Finds spaces in string and removes what is from that space until the space
def remove_irrelevant(string):
    if string.find('<') != -1:
        string = string[0:string.find('<')]
    if string.find('>') != -1:
        string = string[0:string.find('>')]
    if string.find('=') != -1:
        string = string[0:string.find('=')]
    if string.find(',') != -1:
        string = string[0:string.find(',')]    
    if string.find(' ') != -1:
        string = string[0:string.find(' ')]
    if string.find('\'') != -1:
        string = string[0:string.find('\'')]
    if string.find('\"') != -1:
        string = string[0:string.find('\"')]
    if string.find('\)') != -1:
        string = string[0:string.find('\)')]
    if string.find('\(') != -1:
        string = string[0:string.find('\(')]
    
    return string

# Searches for system variables according to pattern and stores it in an output file
def find_basic(readfile, writefile, ext):
    #readfile = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/System Variable List/' + readfile
    readfile = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/findvarinfile/' + readfile
    #readfile = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/BodyShop/' + readfile
    #readfile = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/' + readfile

    pattern = re.compile('[$].+?(?=' + ext + ')')
    with open(readfile, 'r', encoding='latin-1') as t1:
        for line in t1:
            if line.find("POST_ERR") != -1 or line.find("WriteLog") != -1:
                continue
            if line.find("$$") != -1:
                continue
            else:
                p = pattern.findall(line)
                if p:
                    for var in p: 
                        var = remove_irrelevant(var)
                        writefile.write(var + "\n")


if __name__ == '__main__':

    type = input("File or Directory? (f/d): ")
    if type == "f":
        filedir = input("Enter file name: ")
    elif type == "d":
        filedir = input("Enter directory: ")
    else:
        print("Invalid input. Rerun the program")
        sys.exit()

    output = input("Enter output file name: ")
    print()
    if type == "d":
        pot_files = sysfiles(filedir)
    with open(output, 'a+', encoding='latin-1') as out:
        if type == "f":
            ext = fileext(filedir)
            find_basic(filedir, out, ext)
        if type == "d":
            for file in pot_files:
                ext = fileext(filedir)
                filepath = filedir + '/' + file
                find_basic(filepath, out, ext)
    print("""All found potential variables are in """ + output + 
            """\nVariables are now ready for post-processing""")
