'''
Created on Dec 29, 2015

@author: Greg
'''
import os

class FileIO:
    
    
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        
    '''
    Very simple method for writing to a local file.
    '''   
    def write(self, data):
    
        print("Writing output to: %s" % self.path + self.filename)
        
        os.chdir(self.path) #Change to output directory
        
        with open(self.filename, 'w') as f:
            f.write(data)
            f.close()

    '''
    Very simple method for appending data to a local file.
    '''
    def append(self, data):
        print("Appending output to: %s" % self.path + self.filename)
        
        os.chdir(self.path) #Change to output directory
        
        with open(self.filename, 'a') as f:
            f.write(data)
            f.close()   