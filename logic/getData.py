import os
import csv

import pandas as pd
import datetime
from sys import argv
import argparse

from datetime import datetime
from datetime import date

"""
=== ARGPARSE MIGHT BE SUPERIOR ===
In argparse, you can have a mandatory argument, as well as optional arguments,
which are indicated by adding one or two dashes in front of the arg, for instance,
--date
"""
df = pd.read_csv("database/time-spent.csv")


# ======================== TIMEPERIOD FUNCTIONS ========================
# CURRENTLY NONE OF THESE ARE USED.
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

def getHours(action = "Programming", timeperiod= date.today()):
    df_filtered = df[(df.action == action) & (df.date == str(timeperiod))]
    print(str(timeperiod))
    print(df["date"])

# GET SUMMARY OF EACH DAY DURING A SPECIFIED TIMEPERIOD
def getDailyBetween(inputdf):
    print(inputdf[["date", "action", "duration"]].groupby(["date", "action"], as_index=False).sum())

# GET THE TOTAL TIME USED FOR SPECIFIED ACTION/ACTIONS 
def getTotalBetween(inputdf, timespan):
    print(inputdf[[timespan, "action", "duration"]].groupby([timespan, "action"], as_index=False).sum())

# ============================== ERROR HANDLING ==============================
def wrongAction(action):
    print(action)
    wrong_actions = ["week", "year", "date", "month", "day"]
    if action in wrong_actions:
        print("Action must be defined as - or by the name of the action.")
        return

# ============================== MAIN FUNCTIONALITY ==============================
def getSummary(action = "-", duration="date", specify=str(date.today())):
    # Convert timespan columns to strings to avoid search errors.
    df[["year", "week", "month", "day"]] = df[["year", "week", "month", "day"]].astype(str)

    # Filter df based on duration or duration & action.    
    if specify == "total":
        print("TOTAL IS TOTAL")

        # actions_to_search can be altered for your needs. Fetches specified actions by default.
        if (action == "-"):
            actions_to_search = ["Programming", "Vainu", "Gym"]
            df_summary = df[df["action"].isin(actions_to_search) ]
        else:
            print("Searching by: ", action)
            df_summary = df[df["action"] == action]            
        getTotalBetween(df_summary, duration)
    
    else:
        if (action == "-"):
            df_summary = df[df[duration] == specify]
            getDailyBetween(df_summary)
        else:
            try:
                print("Searching by: ", action)
                df_summary = df[(df[duration] == specify) & (df["action"] == action)]            
                getDailyBetween(df_summary)
            except:
                print("Action has to be - or the name of the action. Command structure should be: cal summary [action] [timespan] [specify]")        

# RETURNS USEFUL INFORMATION TO USERS ABOUT THE COMMANDS 
def getHelp():
    print(f'\nTHE STRUCTURE FOR -summary COMMAND: \n {"=" *50}')
    print(" - Can be run without args, which returns a summary of the current day. \n - Can be given 1-3 additional args, specified below.\n")    
    print("cal summary __activity__ __timespan__ __specificity__\n")
    print("__activity__: \n - Can be - in which case default activities are returned. \n - Replace - with activity of interest to fetch information about that.\n")
    print("__timespan__: \n - Can be year/month/week/day \n - Default arg is date, filtering the df by dates\n")
    print("__specify__: \n - By default fetches current date. \n - Can be given a value of total, which gives total hours for specified acitities. \n - Can be given a week/year/day/date, for instance, 45 (week), giving total hours spent on that timeperiod\n")
