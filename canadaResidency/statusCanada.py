#!/usr/bin/env python
# encoding: utf-8
"""
partir-canada.py

Created by Karl Dubost on 2010-11-10.
Modified on 2012-05-31
Copyright (c) 2010 Grange.
Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php.
"""

import time
import datetime
import argparse

# CONSTANT
YEAR = 365
DATEFORMAT = "%Y-%m-%d"
TODAY = datetime.datetime.today()

# Variable initialisation
stay = 0  # count of days spent in Canada


def stringtodate(date, format):
    "convert a string to a datetimeobject (%Y, %m, %d)"
    return datetime.datetime(*time.strptime(date, format)[:3])


def datetostring(date, format):
    "convert a datetimeobject to a string"
    return datetime.datetime.strftime(date, format)


def getLandingDay(data):
    "return the landing day in Canada as a string YYYY-MM-DD"
    return data[0][0]


def getInCan(firstday, data):
    "compute the number of days spent in Canada in between now and firstday"
    # going through the data
    stay = 0
    for (arrival, departure) in data:
        if departure == "now":
            departure = datetostring(TODAY, DATEFORMAT)
            # print "today", departure
        # conversion to datetime object
        adate = stringtodate(arrival, DATEFORMAT)
        ddate = stringtodate(departure, DATEFORMAT)
        if ddate < firstday:
            daysIn = 0
        elif ddate >= firstday:
            if adate > firstday:
                staycountdate = ddate - adate
            else:
                staycountdate = ddate - firstday
            daysIn = staycountdate.days
        stay = stay + daysIn
    return stay


def statusresident(dayssincelanding, firstdaydate, data):
    "compute the status for permanent residency"
    print "-------------------------------------------------"
    print "PERMANENT RESIDENCY: [Rule: 730 min on 1825 days]"
    if dayssincelanding in range(3 * YEAR):
        datestart = firstdaydate
        daysInCanada = getInCan(datestart, data)
        print "%s days in Canada on a total of %s days" % (daysInCanada, dayssincelanding)
    elif dayssincelanding in range(3 * YEAR, 5 * YEAR):
        datestart = firstdaydate
        daysInCanada = getInCan(datestart, data)
        daysOut = dayssincelanding - daysInCanada
        if daysInCanada <= 2 * YEAR:
            print "YOU MUST COME BACK NOW."
        else:
            print "You spent %s days outside on the last %s" % (daysOut, daysInCanada)
            print "Be careful"
    else:
        datestart = TODAY - datetime.timedelta(days=5 * YEAR)
        daysInCanada = getInCan(datestart, data)
        daysOut = (5 * YEAR) - daysInCanada
        if daysInCanada < 2 * YEAR:
            print "YOU MUST COME BACK NOW."
        else:
            print "You spent %s days outside on the last %s" % (daysOut, 5 * YEAR)
            print "You can go out of Canada for %s days" % (daysInCanada - (2 * YEAR))


def citizenship(dayssincelanding, firstdaydate, data):
    "compute when you can apply to citizenship"
    print "-------------------------------------------------"
    print "CITIZENSHIP: [Rule: 1095 min on 1460 days]"
    if dayssincelanding < 3 * YEAR:
        print "TOO EARLY to apply for citizenship."
        print "you need at least 3 years (1095 days)."
    elif dayssincelanding >= 3 * YEAR:
        if dayssincelanding <= 4 * YEAR:
            datestart = firstdaydate
        else:
            datestart = TODAY - datetime.timedelta(days=4 * YEAR)

        daysInCanada = getInCan(datestart, data)
        if daysInCanada < 1095:
            print "TOO EARLY to apply for citizenship"
            print "%s days on 1095 days minimum" % str(daysInCanada)
        else:
            print "CONGRATULATIONS! You can apply"
            print "%s days on 1095 days minimum" % str(daysInCanada)


def parse(FILE):
    "parse the file and put the data in a list"
    data = []
    datafile = FILE.readlines()
    FILE.close()
    # reading line by line the data
    for line in datafile:
        if line.startswith("#"):
            pass
        else:
            arrival, departure = line.split()
            data.append((arrival.replace(' ', ''), departure.replace(' ', '')))
    return data


def main():
    # Parsing the cli
    parser = argparse.ArgumentParser(description="Compute your permanent residency status in Canada")
    parser.add_argument('data', metavar='FILE', help='data file to be processed', action='store', nargs=1, type=argparse.FileType('rt'))
    args = parser.parse_args()
    datafile = args.data[0]
    data = parse(datafile)

    # Get the date of Landing
    landingday = getLandingDay(data)
    # Convert it to date format
    firstdaydate = stringtodate(landingday, DATEFORMAT)
    # How many days since the first arrival
    staycountdate = TODAY - firstdaydate
    # number of days since the first landing (integer)
    dayssincelanding = staycountdate.days
    # Display results
    print "-------------------------------------------------"
    print "Landing: %s" % str(landingday)
    print "Since landing: %s days" % str(dayssincelanding)
    statusresident(dayssincelanding, firstdaydate, data)
    citizenship(dayssincelanding, firstdaydate, data)
    print "-------------------------------------------------"


if __name__ == '__main__':
    main()
