def increase_day(date):

    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])

    if day == 28:  # February check
        if month == 2:
            if year % 4 == 0:
                day = 29
            else:
                month = 3
                day = 1
        else:
            day += 1
    elif day == 29:  # Another February check
        if month == 2:
            month = 3
            day = 1
        else:
            day += 1
    elif day == 30:  # Months with 30 days check
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            day = 31
        else:
            month = str(int(month) + 1)
            day = 1
    elif day == 31:  # Months with 31 days check
        if month == 12:
            year = str(int(year) + 1)
            month = 1
            day = 1
        else:
            month += 1
            day = 1
    else:  # Everything else (from day 1 to day 27 included)
        day = str(int(day) + 1)

    inc_date = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)  # YYYY-MM-DD format

    return inc_date
