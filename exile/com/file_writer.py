'''
Created on Dec 24, 2015

@author: Greg
'''

import os

'''
Very simple function for writing data to a local file.
This will clear the file if it exists and then write.
'''
def writeToFile(path, filename, data, debug=False):
    
    if debug:
        print("Writing output to: %s" % path + filename)
    
    os.chdir(path) #Change to output directory
    
    with open(filename, 'w') as f:
        f.write(data)
        f.close()   
    
    return 0

'''
Very simple function for appending data to a local file.
This will append to the file.
'''
def appendToFile(path, filename, data, debug=False):
    if debug:
        print("Appending output to: %s" % path + filename)
    
    os.chdir(path) #Change to output directory
    
    with open(filename, 'a') as f:
        f.write(data)
        f.close()   
    
    return 0
    
    
    