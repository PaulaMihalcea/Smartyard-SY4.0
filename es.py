from elasticsearch import Elasticsearch
import json

# Local variables
host = 'localhost'
port = 9200

# Database variables
data_file = 'json'
index = 'sensortag'
doc_type = 'sensor_reading'
record_id = 'date'

# Connection to the ElasticSearch cluster
es = Elasticsearch([{'host': host,'port': port}])

# Data file parsing
with open(data_file, 'r') as j:
    data = json.load(j)

# Adds to the ElasticSearch database the previously loaded data
j = 1  # This variable is used to index data records in the right order
for i in data:
   es.index(index=index, doc_type=doc_type, id=j, body=i)  # Adds element to DB
   j += 1
