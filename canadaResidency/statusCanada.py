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
import sys

# CONSTANT
YEAR = 365
STAYMIN = 2 * YEAR  # minimum days in Canada over 5 years
OUTMAX = 3 * YEAR  # maximum days outside Canada over 5 years
CITIZEN = 4 * YEAR  # period for computing the citizenship constraint
COUNTMAX = 5 * YEAR  # maximum period for counting
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


def getInCan(data, firstday, beforefiveyear):
    "compute the number of days spent in Canada since landing"
    # going through the data
    stay = 0
    for (arrival, departure) in data:
        if departure == "now":
            departure = datetostring(TODAY, DATEFORMAT)
            # print "today", departure
        # conversion to datetime object
        adate = stringtodate(arrival, DATEFORMAT)
        ddate = stringtodate(departure, DATEFORMAT)
        if beforefiveyear:
            if ddate < firstday:
                # not counting when it's more than 5 years ago
                daysIn = 0
                pass
            elif ddate >= firstday:
                if adate > firstday:
                    staycountdate = ddate - adate
                else:
                    staycountdate = ddate - firstday
                daysIn = staycountdate.days
        else:
            print sys.exit("not coded yet the case less than 5 years")
        stay = stay + daysIn
    return stay


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

    landingday = getLandingDay(data)
    firstdaydate = stringtodate(landingday, DATEFORMAT)
    # how many days since the first arrival
    staycountdate = TODAY - firstdaydate
    # number of days since the first landing (integer)
    sincelanding = staycountdate.days

    if sincelanding > COUNTMAX:
        beforefiveyear = True
        print "More than 5 years since landing"
        firstcountday = TODAY - datetime.timedelta(days=COUNTMAX)
        print "We count starting", firstcountday
        daysInCanada = getInCan(data, firstcountday, beforefiveyear)
        daysOutCanada = COUNTMAX - daysInCanada
        if daysOutCanada > OUTMAX - 1:
            print "Permanent residency lost"
            print "OutCanada: %s days" % str(daysOutCanada)
        elif daysOutCanada == OUTMAX - 1:
            print "You have to come back today in Canada"
            print "OutCanada: %s days" % str(daysOutCanada)
        elif daysOutCanada < OUTMAX - 1:
            print "Permanent residency is safe"
            print "InCanada:  %s days (minimum %s days on 5 years)" % (str(daysInCanada), str(STAYMIN))
            print "OutCanada: %s days on 5 years" % str(daysOutCanada)
            print "Citizenship Request in %s days (if no trip)" % str(OUTMAX - daysInCanada)
    else:
        print "Less than 5 years since landing"
        beforefiveyear = False

if __name__ == '__main__':
    main()
