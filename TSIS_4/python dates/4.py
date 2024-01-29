from datetime import datetime, time

def date_diff(d2, d1):
    timedelta = d2 - d1
    return timedelta.days * 24 * 3600 + timedelta.seconds

# Specified date
date1 = datetime.strptime('2015-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
# Current date
date2 = datetime.now()
print("\n%d seconds" % (date_diff(date2, date1)))
print()