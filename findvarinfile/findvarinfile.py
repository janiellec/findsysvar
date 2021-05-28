
import re
import os
import csv

def remove_white(string):
    #removes whitespace and after
    if var.find(' ') != -1:
        return var[0:var.find(' ')]
    else:  
        return var

def find_basic(readfile, writefile, ext):
    readfile = '/mnt/c/Users/calaunjr/Desktop/FindSysVar/System Variable List/v833155/' + readfile
    pattern = re.compile('[$].+?(?=' + ext + ')')
    with open(readfile, 'r') as t1:
        for line in t1:
            if line.find("POST_ERR") != -1 or line.find("WriteLog") != -1:
                continue
            else:
                p = pattern.findall(line)
            if p:
                for var in p:
                    var = remove_white(var)
                    writefile.write(var + "\n")

def fileext(name):
    ext = name[name.find('.'):]
    if ext == ".cm":
        return " "
    elif ext == ".xml" or ext == ".stm":
        return "\""
    else:
        return "\'"


if __name__ == '__main__':

    listcheck = input("Enter list of all files to check: ")
    output = input("Enter output file name: ")
    with open(listcheck, 'r') as check, open(output, 'w+') as out:
        list = check.read().splitlines()
        for file in list:
            ext = fileext(file)
            find_basic(file, out, ext)
















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