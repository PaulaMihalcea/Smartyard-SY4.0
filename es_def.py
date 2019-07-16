#def es(host, port, index, doc_type, raw_data_file, save_to):  # TODO Rewrite as function

from elasticsearch import Elasticsearch
from raw2json import raw2json
import time
import json

# Local variables
host = 'localhost'
port = 9200

# Database variables
raw_data_file = 'data2_15_copy'  # TODO Change to default file
save_to = 'data_json'
index = 'sensortag'
doc_type = 'sensor_reading'
period = 20000

# Connection to the ElasticSearch cluster
es = Elasticsearch([{'host': host,'port': port}])

# Data processing cycle
print('Starting data processing cycle...')
j = 1  # This variable is used to index data records in the right order

while True:  # TODO for i in range(0,2):

    # Data file processing
    data = raw2json(raw_data_file, save_to)
    print('Raw data loaded and processed.')

    # Adds to the ElasticSearch database the previously loaded data
    print('Starting POSTs...')
    for i in data:
        es.index(index=index, doc_type=doc_type, id=j, body=i)  # Adds element to DB
        j += 1

    print('Data has been successfully added to database.')
    print(j)

    # Saved data delete
    open(raw_data_file, 'w').close()
    open(save_to, 'w').close()

    time.sleep(period / 1000)

#return 0  # TODO
