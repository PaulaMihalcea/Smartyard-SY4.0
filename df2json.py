def df2json(raw_data_file):

    import json
    from raw2df import raw2df
    from configparser import ConfigParser
    from pprint import pprint  # Pretty print (for readable JSON) - Only needed for debug

    # Local variables
    # raw_data_file = 'data_test'  # Default raw data file (the one containing the data that needs to be processed)
    setup_file = 'setup.ini'  # Setup file (only needed to read the available sensors)
    # save_to = 'data_json'  # Default processed data file (the one which is going to be put in the database)

    # Setup file parsing
    f = ConfigParser()
    f.read(setup_file)  # Parses the setup.ini file

    # Data loading and processing
    df = raw2df(raw_data_file)  # Creates a data frame from the specified raw data file
    df.index.name = 'date'  # Sets the index column name
    df = df.reset_index()  # Resets the index to a column; useful for plotting

    jdict = df.to_dict('records')  # Converts the dataframe in a Python dictionary

    # JSON conversion
    for i in jdict:
        i = json.dumps(i)

    # Open from file - Only needed for debug
    # with open(save_to, 'r') as j:
    #     json_data = json.load(j)
    #     pprint(json_data)

    return jdict
