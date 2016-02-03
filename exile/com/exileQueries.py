'''
Created on Jan 3rd, 2016

Searches for Jewels matching specified properties.

@author: Chris
'''
from com.exile_request import ExileRequest
from com.es_connect import EsConnect
from com.file_writer import writeToFile, appendToFile
from com.mail import Mail
from elasticsearch import Elasticsearch, client
from elasticsearch_dsl import Search, Q
import json
import pprint
import os
import datetime
from datetime import date
from datetime import timedelta
import time
import time
import sys


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
    recepient_address = ""
    email_password = None
    
    #Create an Eslastic Search connection
    esConnect = EsConnect('api.exiletools.com', 80, 'apikey:DEVELOPMENT-Indexer')
    client = esConnect.connect()  
    #date.fromtimestamp(time.time())

    startTime = time.time()
    
    hourMili = 3600000
    dayMili = 86400 * 1000.0
    weekMili = dayMili * 7
    monthMili = weekMili * 4
    currentMili = time.time() * 1000.0
    
    '''
    Time query ranges
    '''  
    #queryLastHour = int(currentMils - hourMili)
    #queryLast12Hours = int(currentMils - (hourMili * 12))
    queryLastDay = int(currentMili - dayMili)
    #queryLastWeek = int(currentMils - weekMili)
    #queryLastMonth = int(currentMils - monthMili) 
    
    
    localtime = time.asctime( time.localtime(time.time()) )
    print('Starting Query at: %s' % localtime)
    
    #Main Query
           
    res = client.search(
      index="index", 
      body={
        "query": {
        "filtered": {
            "query": { "bool": {
             "must": {
                "term" : { "attributes.baseItemType": { "value" : "Jewel" }
              }
            }
          }
        },
        "filter": {
          "bool": {
            "must" : [
                { "term" : { "attributes.league" : "Talisman" } }, 
                { "range": { "shop.chaosEquiv" : { "lte": 50 } } },
                { "range": { "shop.chaosEquiv" : { "gt": 0 } } },
                { "range": { "shop.updated" : { "gte": queryLastDay } } },             
                { "term" : { "shop.verified" : "YES" } }
              ],
            "should" : [
                { "range": { "modsTotal.#% increased Critical Strike Chance with One Handed Melee Weapons": { "gte": 14 } } },
                { "range": { "modsTotal.#% increased maximum Life": { "gte": 5 } } },
                { "range": { "modsTotal.#% increased maximum Energy Shield": { "gte": 6 } } },
                { "range": { "modsTotal.#% increased Critical Strike Chance for Spells": { "gte": 10 } } },
                { "range": { "modsTotal.#% increased Global Critical Strike Chance": { "gte": 6 } } },
                { "range": { "modsTotal.#% increased Melee Critical Strike Chance": { "gte": 10 } } },
                { "range": { "modsPseudo.+#% Total to Elemental Resistances": { "gte": 20 } } },
                { "range": { "modsTotal.+# Mana gained for each Enemy hit by your Attacks": {"gte": 2 } } },
                { "range": { "modsTotal.#% increased Critical Strike Chance with Cold Skills": {"gte": 10 } } },
                { "range": { "modsTotal.#% increased Critical Strike Chance with Elemental Skills": {"gte": 14 } } },
                { "range": { "modsTotal.#% increased Critical Strike Chance with Fire Skills": {"gte": 10 } } },
                { "range": { "modsTotal.#% increased Critical Strike Chance with lightning Skills": {"gte": 10 } } },
                { "range": { "modsTotal.#% increased Critical Strike Multiplier with Cold Skills": {"gte": 10 } } },
                { "range": { "modsTotal.#% increased Critical Strike Multiplier with Elemental Skills": {"gte": 10 } } },
                { "range": { "modsTotal.#% increased Critical Strike Multiplier with Fire Skills": {"gte": 10 } } },
                { "range": { "modsTotal.#% increased Critical Strike Multiplier with lightning Skills": {"gte": 10 } } },
                { "range": { "modsTotal.#% increased Critical Strike Multiplier for Spells": { "gte": 10 } } },
                { "range": { "modsTotal.#% increased Spell Damage while holding a Shield": { "gte": 14 } } },
                { "range": { "modsTotal.#% increased Attack Speed with Daggers": { "gte": 6 } } },
                { "range": { "modsTotal.#% increased Attack Speed while holding a Shield": { "gte": 6 } } },
                                ], "minimum_should_match" : 3
                        }
        }
      }
    }, "size": 100
    } )
    
    localtime = time.asctime( time.localtime(time.time()) )
    print ('Query completed at: %s \n' % localtime)
    endTime = time.time()
    duration = endTime - startTime
    
    result = "Exile Tools Index Result: Got %d Hits and took: %d seconds." % (res['hits']['total'],  duration)
    exceptLimit = 10
    writeToFile(os.curdir, "result.txt", result)
    print result, "\n"
    
    for hit in res['hits']['hits']:
        
        try:
            updated = datetime.datetime.fromtimestamp((hit["_source"]["shop"]["updated"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            modtimestamp = datetime.datetime.fromtimestamp((hit["_source"]["shop"]["updated"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            line =  'Item {fullName} is for sale for {chaosEquiv} by seller {sellerAccount}, last modified on {modified}\n {source}'.format(
            fullName = hit["_source"]["info"]["fullName"], 
            chaosEquiv=hit["_source"]["shop"]["chaosEquiv"], 
            sellerAccount=hit["_source"]["shop"]["sellerAccount"], modified=modtimestamp, 
            source=hit["_source"]["modsTotal"])

            print line
            print
            appendToFile(os.curdir, "result.txt", line)
            appendToFile(os.curdir, "result.txt", "\r\n")
        except:
            print "Unexpected Error:", sys.exc_info()[0]
            exceptLimit -= 1
            if exceptLimit == 0:
                raise
            
    
    #Print the result to the console

    #Write the result to a file.
    writeToFile(os.curdir, "result2.json", json.dumps(res, indent=4))
    
    #Email the result as both the body and as an attached document.
    #The email is commented out by default.
    if sender_address != None and recepient_address != None and email_password != None:
        mail = Mail("smtp.gmail.com")
        mail.connect(sender_address, email_password)
        print("Sending mail")
        mail.send(recepient_address, "test", result, result, "doc.txt")
        print("Mail sent OK")

    
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
    exile_search()
    #exile_query()
    #exile_query2()
    #exile_search()

    pass