def check_file(raw_data_file, attempts, period):

    from datetime import datetime
    import time
    import os

    # Changed day checks (needed because if the sensor device has stopped working there can be "file not found" errors)
    path = './logs/' + raw_data_file  # Dynamic path of the log file
    exists = False  # Flag for new logs (true if a new log has been found, false otherwise)
    attempt_no = 1
    while not exists and attempt_no <= attempts:
        if os.path.isfile(path):  # Checks if the log already exists...
            exists = True  # The new log has been created, so we can continue
        else:  # ...otherwise just goes to the next day, and continues checking
            print('')
            print('Today\'s log not found, waiting for next check... (attempt no. ' + str(attempt_no) + '/' + str(attempts) + ')')
            attempt_no += 1
            time.sleep(period)  # Waits for the next check
    if attempt_no > attempts:
        print('No new log found for today (' + str(datetime.now())[0:10] + '). Maximum number of attempts reached.')

    return exists
