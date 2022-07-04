from fnmatch import fnmatch
import math
import string
import os
clear = lambda: os.system('cls')

def DrawProgress(title, current, total, partitions, errors):
    prog = current / total
    left = math.floor(prog * partitions) 
    right = math.ceil((1 - prog) * partitions)  
    clear()
    print(title)
    print(f'Progress {current}/{total}: [' + "o" * left + "-" * right + "]\n")
    print(f'Error count: {errors}\n')

def DrawComplete():
    print("Complete!")
    input("You can exit now.")

def CollectFilePaths(root, pattern_arr = ["*.*"]):
    list = []
    for pattern in pattern_arr:
        for path, subdirs, files in os.walk(root):
            for name in files:
                if fnmatch(name, pattern):
                    list.append(os.path.join(path, name))
    return list

def MakeDirsIfNotExist(p):
    if not os.path.exists(os.path.dirname(p)):
            os.makedirs(os.path.dirname(p))    

def IsPathExists(p):
    return os.path.exists(p)

def DeleteFileIfExists(file):
    if os.path.exists(file):
        os.remove(file)
    return

def WriteToLog(file, msg):
    f = open(file, "a")
    f.write(msg)
    f.close()
    return

def DeleteCharactersFromString(str,symbols):
    return str.translate({ord(i):None for i in symbols})

def FilterFileName(str,symbols):
    name = os.path.basename(str)
    name = DeleteCharactersFromString(name,symbols)
    return os.path.join(os.path.dirname(str),name)