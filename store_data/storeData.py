import datetime
from datetime import datetime, date, timedelta
import dateutil.parser
import pandas as pd
from pandas import DataFrame

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
from os import path

# ======================== CHANGE THIS TO FETCH DATA BEGINNING FROM THIS DATE ========================
from_date = date(2022, 8, 29)  # 2022, 8, 29 Google API only fetches 250 rows of data per call. Need to fix this!

def csvExists():
    if os.path.exists('database/time-spent.csv'):
        return True
    return False

# Completely overwrites existing CSV, if there is one.

def csvHandler(input, update=False, update_from=False): # Receives df
    if csvExists() and not update:
        print("Appending data to existing db")
        input.to_csv('database/time-spent.csv', mode='a', index=False, header=False)
    
    elif csvExists() and update:
        print("WORK IN PROGRESS")
        # Overwrite beginning from a certain point in time. not sure how done.

        cdf = pd.read_csv('database/time-spent.csv')
        cdf['date'] = pd.to_datetime(cdf['date'])
        print("updating from: ", update_from)
        cdf = cdf[~(cdf['date'] >= update_from)]
        
        updated_df = pd.concat([cdf, input])
        updated_df.to_csv('database/time-spent.csv', index=False)
        
    else:
        os.makedirs('database', exist_ok=True)
        input.to_csv('database/time-spent.csv', index=False)
        

def buildDf(api_events):
            
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

        for event in api_events:

            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            new_start = dateutil.parser.isoparse(start) # changing the start time to datetime format
            new_end = dateutil.parser.isoparse(end) # changing the end time to datetime format

            readable_start = new_start.strftime("%H:%M")
            readable_end = new_end.strftime("%H:%M")

            # Create columns & row data
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
            
        # Create the dataframe and save it to csv.
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
        append_df = pd.DataFrame.from_dict(dictory)
        return append_df


# Fetch data between dates X and Y and store in csv.
def fetchAndStoreData(creds, to_date = date.today()):    
    try:
        service = build('calendar', 'v3', credentials=creds)

        print(to_date)

        # If a df exists, overwrite from the day we have data from.
        if csvExists():
            with open('database/time-spent.csv', 'r') as csv:
                existing_data_to = datetime.strptime([[x.strip() for x in line.strip().split(',')] for line in csv.readlines()][-1][1], "%Y-%m-%d")
            updateData(creds, existing_data_to, to_date) 
            return
        
        else:
            startTime = str(from_date) + "T00:00:00Z"
            endTime = str(to_date) + "T23:59:59Z"
        

        print("start time: ", startTime)
        events_result = service.events().list(calendarId='primary', timeMin=startTime, timeMax=endTime,
                                                singleEvents=True,
                                                orderBy='startTime', timeZone="Europe/Helsinki").execute()
        events = events_result.get('items', [])

        if not events:
            return

        time_df = buildDf(events)
        csvHandler(time_df)

    except HttpError as error:
        print('An error occurred: %s' % error)


# Fetch data beginning from date X and overwrite from there.
def updateData(creds, date_from, to_date = date.today()):
    try:
        service = build('calendar', 'v3', credentials=creds)

        startTime = str(date_from.strftime('%Y-%m-%d')) + "T00:00:00Z"
        endTime = str(to_date) + "T23:59:59Z"

        events_result = service.events().list(calendarId='primary', timeMin=startTime, timeMax=endTime,
                                                singleEvents=True,
                                                orderBy='startTime', timeZone="Europe/Helsinki").execute()
        events = events_result.get('items', [])
        if not events:
            return

        time_df = buildDf(events)
        csvHandler(time_df, True, date_from)

    except HttpError as error:
        print('An error occurred: %s' % error)


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

