def min_date(last_dates):

    minimum = '9999-13'  # (almost) Impossible maximum to make sure the actual minimum date in last_dates will be selected; remember to update after year 9999 (possibly to something like 99999)
    for d, v in last_dates.items():
        if v < minimum:
            minimum = v

    return minimum[0:10]
