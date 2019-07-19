def update_db(raw_data_file, last_dates, es, index, doc_type):

    from modules import df2json as d
    from datetime import datetime

    # Raw data file processing (raw to dataframe, then dataframe to json)
    raw_data_file = 'logs/' + raw_data_file
    data = d.df2json(raw_data_file)
    status = False

    # Adds to the ElasticSearch database the previously loaded data
    for e in data:
        for d, v in last_dates.items():
            if e['MAC'] == d and v < e['date']:  # Adds new data to database only if more recent than the last item added for the current device (saved in the specific file last.date)
                es.index(index=index, doc_type=doc_type, body=e)  # Adds element to DB with an automatically generated unique id
                last_dates[d] = e['date']
                status = True
            else:
                pass

    with open('config/last.date', 'w') as f:
        f.write(str(last_dates))  # Overwrites the contents of the last.date file with the new, updated date

    return status
