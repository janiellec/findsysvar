# FINDING SYSTEM VARIABLES OF MULTIPLE FILES

This project is supposed to find system variables (formatted as "$<variable name>")
in multiple files. 

## by JANIELLE CALAUNAN as FANUC BSG SWE Intern

The project currently consists of two scripts: findvarinfile.py and check_exist.py. The latter was much more useful in the early stages of the project where individual programs were needed to check the find system variables. This is now optimized so that findvarinfile.py is the only script needed to find system variables.

This is my first Python project, which was learned as these programs grew and were written. While it was incredibly fun to make (despite being a fairly simple task), it isn't perfect. There are plenty of nested loops that might make it run faster (big O is pretty big considering how many lines are in each file and how many files are in the folder). There also seems to be some bugs here and there which can easily be found during the post-processing stage of the project.

That said, here are the script I wrote for this project

### check_exist.py
This program takes in a list of files that are supposed to have system variables and compares it to a list of all the possible files to double check spelling. This program calls for 3 user inputs and has two functions within it.

**setup_files(set_name, directory)**:
This function creates a file of all file names in a directory. It takes in *set_name*, received from user input, of all the files in a given *directory* (under the where all the system variable files are). Note that because the user only needed to input the output file name *without* an extension or absolute file path, the original code included my file path under <filepath>. This also lead to extra lines just to make sure the program finds the files. I wanted the file to be a csv file but it probably would have been easier and might have taken less debugging if I used a simple text file.
  
```python
setup_files(set_name, directory)
    setcsv = open(set_name + '.csv', "w")
    setup_file = csv.writer(setcsv)
    string = (<filepath>, directory)
    dire = "".join(string)
    for root, dir, files in os.walk(dire):
        for all in files:
            setup_file.writerow([all])
```

**file_exist(list, setup)**: This function did all of the dirty work. It takes in *list*, a csv file of a list of potential files that have system variables in them, and the newly created file, *setup*, which is also a csv file. It is fairly simple. First, it collects all the lines from each csv file and turns it into a list. It then compares files in the list of potential files with all the files in the directory and if it didn't find it, it adds it to a file of all misspelled filenames in not_exist.csv.

```python
file_exist(list, setup):
    with open(list, 'r') as t1, open(setup, 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()
        print(filetwo)
    filestatus = False                                  #nothing in not_exist file
    with open('not_exist.csv', 'w') as outfile:
        for line in fileone:
            if line not in filetwo:
                outfile.write(line)
                filestatus = True                       # at least 1 thing in not_exist file
    if filestatus is False:                             # less than 1 thing in not_exist file
        print('All files correct')
        os.remove("not_exist.csv")
```

check_exist then returns a list of items that don't exist or creates nothing, which indicates that all files exist in the potential file list.
  
### findvarinfile.py
This program takes in a file directory from which system variables (format as described above) can be found and creates a list of all the variables found. This is the most updated version. It takes in 2 user inputs.
  
**sysfiles(directory)**: This function searches all the files in a *directory* if it has a certain character in it. If the file does have the character (in this case, $), it adds the file to a list of other files that include the character. It uses a helper function called **search(list, character)** that takes in a *list*, reads into them, and searches for the *character*.

```python
sysfiles(directory):
    path = <filepath> + directory
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
```

**fileext(name)**: Not all files being read uses the same demarcation to signal the end of a system variable. Since I only need to search through certain files, I only used the demarcation those files.
```python
fileext(name):
    ext = name[name.find('.'):]
    if ext == ".cm":
        return " "
    elif ext == ".xml" or ext == ".stm":
        return "\""
    else:
        return "\'"
```
  
**remove_white(string)**: In some cases, extra white space exists in the found function. Usually, a space and beyond are different parts of a comment or a line of code. In order to get rid of those, remove_white finds the first white space and deletes everthing after, or more accurately, only takes in up until the whitespace.
```python
remove_white(string):
    if string.find(' ') != -1:
        return string[0:string.find(' ')-1]
    else:  
        return string
```
  
**find_basic(readfile, writefile, ext)**: This function does most of the heavy listing of actually finding the system variables using RegEx and prints each out on an output file. It skips lines that begin with POST_ERR or WriteLog since those just repeat the function and are essentially just comments.
```python
find_basic(readfile, writefile, ext):
    readfile = <filepath> + readfile
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
```
  
The final main function takes in the folder to find the files in and a desired output file name. The final step is then post-processing

## Post-Processing

The post-processing of the system variables is simple but tedious. There are plenty of special cases to the formatting of each system variables, depending on loops, comments, files, etc. 
Manual post-processing necessary to find special cases such as:

1. '$\_\_something\_\_[' + variable + '].$\_\_somelse\_\_[' + number + ']
    - premature termination
    - searches for this second $ and demarcation while variable is not finished
    - need to double check that every $....[ is closed off or includes the second part connected to it as opposed to separate
2. '$\_\_something\_\_' + number + '[' + number + '].$\_\_someelse\_\_'
    - premature termination
    - need to include gun number
  
Because of these special cases, they need to be found so that only complete variables are found and $\_\_somelse\_\_ isn't recorded as its own variable. This post-processing is done in excel.
