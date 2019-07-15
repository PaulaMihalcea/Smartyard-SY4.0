from elasticsearch import Elasticsearch
import json

# Connect to the elastic cluster
es = Elasticsearch([{'host':'localhost','port':9200}])

# print(es)


e1 = {
    'date': '2019-07-12 14:48:46.415',
    'opt': '10 00',
    'hum': '20 68 f8 61',
    'bar': 'a8 0a 00 2c 89 01',
    'mov': 'c3 ff 06 01 2d 00 35 00 16 00 91 f7 7c 03 00 ff 4d fe',
    'temp': 'd4 0a 74 0d',
    'id': '0'
}

# print(e1)

#res = es.index(index='sensortag',doc_type='sensor_reading',id=1,body=e1)  # Add element to DB

# res=es.get(index='sensortag',doc_type='sensor_reading',id=1)  # Search for element by query

#res=es.delete(index='sensortag',doc_type='sensor_reading',id=1)  # Delete a document

# print(res['result'])  # Prints the result of a DELETE command

#print(res)

with open('json', 'r') as j:
    json_data = json.load(j)
    # print(json_data)


# Aggiunge al DB gli elementi caricati dal file
# for el in json_data:
#      print(el['date'])
#      res = es.index(index='sensortag',doc_type='sensor_reading',id=el['date'],body=el)  # Add element to DB

# res=es.get(index='sensortag',doc_type='sensor_reading',id=45)  # Search for element by query

# SCRIPT GENERALE PER CANCELLARE X RECORD DAL DB
# for i in range(1,362):
#     res=es.delete(index='sensortag',doc_type='sensor_reading',id=i)
#     print(res['result'])

# print(es.get(index='sensortag',doc_type='sensor_reading',id='2019-07-12 14:56:48.234'))

# print(res)

print(es.search(index="sensortag", body={"query": {"prefix" : { "id" : "2019-07-12" }}}))
