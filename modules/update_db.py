def update_db(raw_data_file_path, es, index, doc_type, attempts, period):

    from modules import df2json as d
    import time

    # Raw data file processing (raw to dataframe, then dataframe to json)
    data = d.df2json(raw_data_file_path)
    status = False  # Flag to return to the calling function; it says whether new entries have been added to the database or not

    # last.dates file reading
    attempt_no = 1  # Number of attempts to read the last.dates file; the whole following block is a fix to an EOF exception that appears at times when trying to read the said file
    while True:
        try:
            with open('config/last.date', 'r') as f:
                last_dates = eval(f.read())
        except Exception:
            print('Error while trying to read last.dates file, waiting for next check... (attempt no. ' + str(attempt_no) + '/' + str(attempts) + ')')
            attempt_no += 1
            time.sleep(period)
            if attempt_no > attempts:
                print('Error while trying to read last.dates file, maximum number of attempts reached. Exiting program.')
                exit()
            else:
                continue
        else:
            break

    # Adds to the ElasticSearch database the previously loaded data
    for e in data:
        for r, v in last_dates.items():
            if e['MAC'] == r and v < e['date']:  # Adds new data to database only if more recent than the last item added for the current device (saved in the specific file last.date)
                es.index(index=index, doc_type=doc_type, body=e)  # Adds element to DB with an automatically generated unique id
                last_dates[r] = e['date']  # Updates the last database update date (Warning: too many dates)
                status = True
            else:
                pass  # Ignores an entry if it is already present in the database

    with open('config/last.date', 'w') as f:
        f.write(str(last_dates))  # Overwrites the contents of the last.date file with the new, updated date

    return status
