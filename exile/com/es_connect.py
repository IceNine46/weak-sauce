'''
Created on Dec 24, 2015

@author: Greg
'''

import elasticsearch

class EsConnect(object):
    '''
    This class will return an elastic search connection.
    
    ExileTools api:
    host: 'api.exiletools.com'
    port: 80
    http_auth: 'apikey:DEVELOPMENT-Indexer'
    '''

    def __init__(self, host, port, apiKey):
        self.host = host
        self.port = port
        self.apiKey = apiKey 
    
    def connect(self):
        client = elasticsearch.Elasticsearch([{
                                               'host':self.host,
                                               'port':self.port,
                                               'http_auth':self.apiKey,
                                               'timeout':50
                                               }])
        elasticsearch.Connection
        return client
    