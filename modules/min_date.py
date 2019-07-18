def min_date(last_dates):

    min = '9999-13'
    for d, v in last_dates.items():
        if v < min:
            min = v

    return min[0:10]
