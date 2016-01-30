'''
Created on Dec 23, 2015

A basic driver program for executing a simple elastic search query through the exiletools index.
This method uses the a basic dict approach for the queries.

This driver contains a few examples for executing different queries and parsing the JSON results.

@author: Greg
'''
from com.exile_request import ExileRequest
from com.es_connect import EsConnect
from com.file_writer import writeToFile
from com.mail import Mail
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import json
import pprint
import os
from com.file_io import FileIO


dashes = "-----------------------------------------------------------------"

'''
    Connection Info
    ExileTools api:
    host: 'api.exiletools.com'
    port: 80
    http_auth: 'apikey:DEVELOPMENT-Indexer'
'''

'''
EXAMPLE Exile Tools Elastic Search


Find how many rings are available.

Then:
1.) Print the result to the console.
2.) Write the result to a file.
3.) Email the result.

'''

def exile_search():
    '''
    Email Settings
    sender_address = "your.email@gmail.com" 
    recepient_address = "recepient.email@gmail.com" 
    email_password = "your password"
    ''' 
    sender_address = None
    recepient_address = None
    email_password = None
    
    #Create an Eslastic Search connection
    esConnect = EsConnect('api.exiletools.com', 80, 'apikey:DEVELOPMENT-Indexer')
    client = esConnect.connect()         
    
    res = client.search("index", body={
                                       
      "aggs" : {
      "leagues" : {
        "terms" : { 
          "field" : "attributes.league",
          "min_doc_count":5000,
          "size":0              
            }
          }
        },   
      "query" : {
        "filtered" : {
          "filter" : {
            "bool" : {
              "must" : [        
                { 
                  "term" : { 
                  "attributes.equipType": "Ring" 
                  } 
                }
              ]
            }
          }
          }
      },
      "sort": [
        {
          "shop.chaosEquiv": {
            "order": "asc"
          }
        }
      ],
      "size": 100
    } )
    
    result = "Exile Tools Index Result: Got %d Hits" % res['hits']['total']
    #Print the result to the console
    print(result)
    
    #Write the result to a file.
    writeToFile(os.curdir, "result.txt", result)
    
    #Email the result as both the body and as an attached document.
    #The email is commented out by default.
    if sender_address != None and recepient_address != None and email_password != None:
        mail = Mail("smtp.gmail.com")
        mail.connect(sender_address, email_password)
        print("Sending mail")
        mail.send(recepient_address, "test", result, result, "doc.txt")
        print("Mail sent OK")

    
    return 0

def exampleWriteMultiple(writer):
    
     #Create an Eslastic Search connection
    esConnect = EsConnect('api.exiletools.com', 80, 'apikey:DEVELOPMENT-Indexer')
    client = esConnect.connect()         
    
    res = client.search("index", body={
                                         
      "query" : {
        "filtered" : {
          "filter" : {
            "bool" : {
              "must" : [        
                { 
                  "term" : { 
                  "attributes.equipType": "Ring" 
                  } 
                }
              ]
            }
          }
          }
      },
      "size": 100
    } )
    result = "Exile Tools Index Result: Got %d Hits\n" % res['hits']['total']
    
    '''
    Here is an example of writing multiple strings to a file with one call.
    You can concatenate strings together using the "+" operator.
    Here is an example using a variable:
    concatResult = '**** Start of Output ****\n\n' + 'Writing output on one write call\n\n' + result + '\n\n**** End of Output****\n\n' 
    
    json.dumps(res, indent=4) - This takes the JSON response and formats it nicely into a string.
    '''  
    writer.write('**** Start of Output ****\n\n' + 'Writing output on one write call\n\n' + result + '\n**** End of Output****\n\n')
    
    '''
    Here is an example of writing multiple strings separately.
    '''
    writer.append("**** Start of Output ****\n\n")
    writer.append("Writing output on multiple write calls.\n\n")
    writer.append( result)
    writer.append("Raw JSON Result:\n\n")
    writer.append(json.dumps(res, indent=4))
    writer.append('\n**** End of Output****\n\n')
    
    return 0

'''
More Exile Query examples

***The following example requests DO NOT use the elastic search api interface.
They go directly at the http endpoint and return the json response.

The body request is a JSON elastic search query.

  Example query against the _mapping index. The _mapping index is used to get the data organization
  for the various mods.
  
  This url will get you the entire _mapping layout.
   http://api.exiletools.com/index/_mapping?pretty - This is a large file.
'''
def exile_query():
    
    apiKey = "DEVELOPMENT-Indexer"
    request = ExileRequest("http://api.exiletools.com/index/_mapping/field/shop.*?pretty", apiKey, None)
    result = request.execute()
    #dashes = "-----------------------------------------------------------------"
    #print the entire result
    print("Running exile_query")
    print(dashes)
    print("Print the entire query result:")
    pprint.pprint(result)
    print(dashes)
    
    #Create a shortcut dictionary

    tmp_dic = result['poe']['mappings']['item']
    
    #print just the entries for the shop.added key
    
    print("Print just the shop.added nodes.")
    pprint.pprint(tmp_dic['shop.added'])
    print(dashes)
    
    #get the shop.added key value and assing to a variable
    shopAddedName = tmp_dic['shop.added']['full_name']
    
    #print a message with the variable
    print('This is the shop.added name: %s' % shopAddedName)
    print(dashes)
    
    return 0

'''
Example exile query passing a elasticquery as a dictionary.

This example driver prints the JSON output to the console and writes the output to a local file.
'''
def exile_query2():
    
    #apiKey = "DEVELOPMENT-Indexer"
    
    url = "http://api.exiletools.com/index/_search?search_type=count&pretty" 
    query ='{\
            "aggs":{\
                "leagues":{\
                    "terms": {"field": "attributes.league", "min_doc_count":5000,"size": 0}\
                            }\
                     }\
             }'
    
    request = ExileRequest(url,None, query)
    result = request.execute()
    print("Running exile_query2")
    print(dashes)
    #print the entire result
    
    print("Print the entire query result:")
    pprint.pprint(result)
    print(dashes)
    
    writeToFile(os.curdir, "test.json", json.dumps(result, indent=4))
    
    return 0


'''
MAIN DRIVER
Uncomment other examples to execute.
'''
if __name__ == '__main__':
    
    '''
    Here we create a FileIO Object and now we can just pass this object along to the different functions,
    and they can all keep appending to the file without having to specify the filename and the path.
    Though they could change it and write to another file.
    '''
    writer = FileIO(os.curdir, "result.txt")
    
    exampleWriteMultiple(writer)
    #exile_search()
    #exile_query()
    #exile_query2()
    #exile_search()

    pass