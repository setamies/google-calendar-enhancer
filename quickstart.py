from __future__ import print_function

import datetime
from datetime import time
import os.path
import dateutil.parser

import pandas as pd
from pandas import DataFrame
import numpy as np
import sys
from sys import argv

import os
import logic

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] # Removing the .readonly will make enable modifying cal


# ==================================FUNCTION SECTION==================================
def csvHandler(input):
    os.makedirs('database', exist_ok=True)
    input.to_csv('database/time-spent.csv', index=False)

def getComingEvents(service): 
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])




# Completely overwrites existing CSV, if there is one. Fetch data between dates X and Y and store in csv.
def setEvents(service):
    from_date = datetime.date(2022, 8, 29)
    today = datetime.date.today()
    
    # Define the time period you want to fetch data from
    startTime = str(from_date) + "T00:00:00Z"
    endTime = str(today) + "T23:59:59Z"

    events_result = service.events().list(calendarId='primary', timeMin=startTime, timeMax=endTime,
                                              singleEvents=True,
                                              orderBy='startTime', timeZone="Europe/Helsinki").execute()
    events = events_result.get('items', [])

    if not events:
        return

    year_col = []
    week_col = []
    date_col = []
    month_col = []
    day_col = []
    start_times = []
    end_times = []
    actions = []
    durations = []
    machine_readable_start = []
    machine_readable_end = []

    for event in events:

        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        new_start = dateutil.parser.isoparse(start) # changing the start time to datetime format
        new_end = dateutil.parser.isoparse(end) # changing the end time to datetime format

        readable_start = new_start.strftime("%H:%M")
        readable_end = new_end.strftime("%H:%M")

        # Create columns & row data
        # YEAR WEEK DAY DATE ACTION START END DURATION UGLYSTART UGLYEND
        year = new_start.strftime("%Y")
        week = new_start.isocalendar()[1]
        date = new_start.strftime("%Y-%m-%d")
        month = new_start.strftime("%m")
        day = new_start.strftime("%d")

        year_col.append(year)
        week_col.append(week)
        date_col.append(date)
        month_col.append(month)
        day_col.append(day)
        machine_readable_start.append(new_start)
        machine_readable_end.append(new_end)
        start_times.append(readable_start)
        end_times.append(readable_end)
        actions.append(event["summary"])
        durations.append((new_end - new_start).seconds/60/60)
        
    # Create the dataframe 
    dictory = {
        "year": year_col,
        "date": date_col,
        "week": week_col,
        "month": month_col,
        "day": day_col,
        "start": start_times,
        "end": end_times,
        "action": actions,
        "duration": durations,
        "string-start": machine_readable_start,
        "string-end": machine_readable_end
    }

    time_df = pd.DataFrame.from_dict(dictory)
    csvHandler(time_df)
    
def commitHours(creds):    
    try:
        # Could make the upcoming events to a function.
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        setEvents(service)

    except HttpError as error:
        print('An error occurred: %s' % error)

# ==================================MAIN SECTION==================================

def main():
    """
    Main function simply connects to the API
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    #logic.getData()

    if argv[1] == 'get':
        print("Work in progress")

    elif argv[1] == 'summary':
        # Not very elegant, try to find a better way to express this        
        if len(sys.argv)  == 2:
            logic.getSummary()
        elif len(sys.argv) == 3:
            logic.getSummary(argv[2])
        elif len(sys.argv) == 4:
            logic.getSummary(argv[2], argv[3])
        elif len(sys.argv) == 5:
            logic.getSummary(argv[2], argv[3], argv[4])            
        elif len(sys.argv) == 6:
            logic.getSummary(argv[2], argv[3], argv[4], argv[5])  

    elif argv[1] == 'store-data':
        commitHours(creds)
    elif argv[1] == 'help':
        logic.getHelp()
            

    #logic.getHours()

if __name__ == '__main__':
    main()
