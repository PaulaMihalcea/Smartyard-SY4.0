def notify(event, message, setup_file_number, device_mac):

    from configparser import ConfigParser
    from elasticsearch import Elasticsearch
    from datetime import datetime

    # Setup
    f = ConfigParser()
    if int(setup_file_number) == 1:
        f.read('config/setup_db.ini')  # Parses the setup_db.ini file
    else:
        f.read('config/setup_db' + setup_file_number + '.ini')  # Parses the setup_db.ini file with the corresponding number (e.g. setup_db2.ini, etc.)

    host = f.get('database', 'host')
    port = f.get('database', 'port')
    index = str(f.get('database', 'notify_index'))
    doc_type = str(f.get('database', 'notify_doc_type'))

    # Connection to the ElasticSearch cluster
    es = Elasticsearch([{'host': host, 'port': port}])

    e = {'date': str(datetime.now().strftime('%Y-%m-%d.log')), 'device_mac': device_mac, 'event': event, 'message': message}

    # Event dispatch to the database
    es.index(index=index, doc_type=doc_type, body=e)  # Adds element to DB with an automatically generated unique id

    return
