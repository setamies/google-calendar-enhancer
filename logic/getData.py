import pandas as pd
import datetime
from sys import argv
import argparse

from datetime import datetime
from datetime import date
# Get events 

    # Might need this df.duration = pd.to_timedelta(df['duration'])


"""
Make this class and functions be able to filter the dataframe in various ways.

GET YEARLY DATA
GET DATE DATA
GET WEEKLY DATA
GET MONTHLY DATA
GET DAILY DATA

- First run one of the two kinds of functions
- Then input some arguments

=== ARGPARSE MIGHT BE SUPERIOR ===
In argparse, you can have a mandatory argument, as well as optional arguments,
which are indicated by adding one or two dashes in front of the arg, for instance,
--date

"""

df = pd.read_csv("database/time-spent.csv")
parser = argparse.ArgumentParser(description = "")

parser.add_argument("")


# ======================== TIMEPERIOD FUNCTIONS ========================



def getWeeklyData(year):
    return df[df.year == year]

# format as yyyy-mm-dd
def getDateData(date):
    df = pd.read_csv("database/date-spent.csv")
    return df[df.date == date]

# year as an optional argument
def getWeeklyData(week, year = datetime.now().year):
    return df[df.week == week]

def getMonthlyData(month, year = datetime.now().year):
    return df[df.month == month]

def getDailyData(day, month = datetime.now().month, year = datetime.now().year):
    return df[df.month == month]

# ======================== FILTERING FUNCTIONS ========================

# Get hours for a specific action, which is programming by default.

"""
usage: py google-calendar-enchancer.py ...

...summary

...get year/month/week/day action int   

"""
def getHours(action = "Programming", timeperiod= date.today()):
    df_filtered = df[(df.action == action) & (df.date == str(timeperiod))]
    print(str(timeperiod))
    print(df["date"])


# Can't remember the one command :/
def getSummary():
    df_summary = 