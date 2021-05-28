
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
    path = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/System Variable List/' + directory
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
    if ext == ".cm":
        return " "
    elif ext == ".xml" or ext == ".stm":
        return "\""
    else:
        return "\'"

# Finds spaces in string and removes what is from that space until the space
def remove_white(string):
    if string.find(' ') != -1:
        return string[0:string.find(' ')-1]
    else:  
        return string

# Searches for system variables according to pattern and stores it in an output file
def find_basic(readfile, writefile, ext):
    readfile = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/System Variable List/' + readfile
    pattern = re.compile('[$].+?(?=' + ext + ')')
    with open(readfile, 'r', encoding='latin-1') as t1:
        for line in t1:
            if line.find("POST_ERR") != -1 or line.find("WriteLog") != -1:
                continue
            else:
                p = pattern.findall(line)
            if p:
                for var in p:
                    var = remove_white(var)
                    writefile.write(var + "\n")

if __name__ == '__main__':

    filedir = input("Enter directory under System Variable List: ")
    output = input("Enter output file name: ")
    
    print('\n')
    pot_files = sysfiles(filedir)
    with open(output, 'w+', encoding='latin-1') as out:
        for file in pot_files:
            ext = fileext(file)
            filepath = filedir + '/' + file
            find_basic(filepath, out, ext)
    print("""All found potential variables are in """ + output + 
            """\nVariables are now ready for post-processing""")






#################################################################################################################
#################################################################################################################
################################# code that only partially works ################################################
#################################################################################################################
#####  MAIN ISSUE:  #############################################################################################
#####       only reads the first variable in the line  ##########################################################
#################################################################################################################
#################################################################################################################
#
#def remove_white(string):
#    #removes whitespace and after
#    if var.find(' ') != -1:
#        return var[0:var.find(' ')]
#    else:  
#        return var

#def find_basic(readfile, writefile):
#    pattern = re.compile('[$].+?(\[.\])??.+?(\[.\])??(?=\'|\")')
#    #dirc = "/mnt/c/Users/calaunjr/Desktop/FindSysVar/System Variable List/v833155/"
#    #readfile = dirc + readfile
#    with open(readfile, 'r') as t1:
#        for line in t1:
#            if line.find("POST_ERR") != -1 or line.find("WriteLog") != -1:
#                continue
#            else:
#                p = pattern.search(line)
#            #if p != None:
#            #    var = p.group()
#            #    var = remove_white(var)
#            #    if var not in writefile:
#            #        writefile.write(var + "\n")

#            if p != None:
#                writefile.write(p.group() + "\n")

#if __name__ == '__main__':
   
#    listcheck = input("Enter list of all files to check: ")
#    output = input("Enter output file name: ")
#    with open(listcheck, 'r') as check, open(output, 'w+') as out:
#        list = check.read().splitlines()
#        for file in list:
#            # file += ".kl"
#            find_basic(file, out)
#    print("\n")