import datetime
import dateutil.parser
import pandas as pd
from pandas import DataFrame

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

# ======================== CHANGE THIS TO FETCH DATA BEGINNING FROM THIS DATE ========================
from_date = datetime.date(2022, 8, 29)




# Completely overwrites existing CSV, if there is one.
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

# Fetch data between dates X and Y and store in csv.
def fetchAndStoreData(creds, to_date = datetime.date.today()):    
    try:
        # Could make the upcoming events to a function.
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        print(to_date)

        # Define the time period you want to fetch data from
        startTime = str(from_date) + "T00:00:00Z"
        endTime = str(to_date) + "T23:59:59Z"

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
        time_df = pd.DataFrame.from_dict(dictory)
        csvHandler(time_df)

    except HttpError as error:
        print('An error occurred: %s' % error)