import calendar
from datetime import date, timedelta


def date_range_list(start_date, end_date):
    try:
        firstdate = start_date.split('/')
        seconddate = end_date.split('/')
        start_date = date(int(firstdate[2]), int(firstdate[0]), int(firstdate[1]))
        end_date = date(int(seconddate[2]), int(seconddate[0]), int(seconddate[1]))
        if start_date > end_date:
            return "You have entered an improper date range please try again"
        if abs((end_date - start_date).days) > 22:
            return "You have entered a date range too large, please be in a range under 21 days"
        # difference between current and previous date
        delta = timedelta(days=1)
        # store the dates between two dates in a list
        dates = []
        while start_date <= end_date:
            # add current date to list by converting  it to iso format
            #print(start_date)
            day = calendar.day_name[start_date.weekday()]
            dates.append(f'{day}, {calendar.month_name[start_date.month]} {start_date.day}, {start_date.year}')
            # increment start date by timedelta
            start_date += delta
        return dates
    except:
        return "You have entered an improper date please try again."

