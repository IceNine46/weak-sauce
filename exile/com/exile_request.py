'''
Created on Dec 23, 2015

@author: Greg
'''

import urllib2, json

class ExileRequest(object):
    '''
    Connect to the exile tools server index without using elastic search.
    This is a very basic way of getting data from the index.
    '''
    
    '''
        Init the ExileRequest object
    '''
    def __init__(self, url, apiKey, query):
        self.url = url
        self.query = query 
        
        #Try to use the default developer api key if None is passed.
        if apiKey == None:
            self.apiKey = "DEVELOPMENT-Indexer"
        else:
            self.apiKey = apiKey
        
    '''
        Basic getters and setters for class instance variables.
    '''        
    def getUrl(self):
        return self.url
    
    def getapiKey(self):
        return self.apiKey
    
    def getQuery(self):
        return self.query
    
    def setUrl(self, url):
        self.url = url
        
    def setApiKey(self, apiKey):
        self.apiKey = apiKey
        
    def setQuery(self, query):
        self.query = query
         
    '''
        Executes a http request against the provide URL, with the passed Elasticesearch query.
        Returns the JSON response.
    '''
    def execute(self):
    
        request = urllib2.Request(self.url, self.query, {'Content-Type': 'application/json'})
        request.add_header("Authorization", self.apiKey)
        r = urllib2.urlopen(request)
        
        result = json.load(r.fp)
   
        r.close()
       
        return result
    
    

