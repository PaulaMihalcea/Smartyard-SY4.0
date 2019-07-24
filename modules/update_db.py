def update_db(raw_data_file, last_dates, es, index, doc_type):

    from modules import df2json as d

    # Raw data file processing (raw to dataframe, then dataframe to json)
    raw_data_file = 'logs/' + raw_data_file
    data = d.df2json(raw_data_file)
    status = False  # Flag to return to the calling function; it says whether new entries have been added to the database or not

    # Adds to the ElasticSearch database the previously loaded data
    for e in data:
        for d, v in last_dates.items():
            if e['MAC'] == d and v < e['date']:  # Adds new data to database only if more recent than the last item added for the current device (saved in the specific file last.date)
                es.index(index=index, doc_type=doc_type, body=e)  # Adds element to DB with an automatically generated unique id
                last_dates[d] = e['date']  # Updates the last database update date (Warning: too many dates)
                status = True
            else:
                pass  # Ignores an entry if it is already present in the database

    with open('config/last.date', 'w') as f:
        f.write(str(last_dates))  # Overwrites the contents of the last.date file with the new, updated date

    return status
