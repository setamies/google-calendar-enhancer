from __future__ import print_function

import os.path

import pandas as pd
from pandas import DataFrame
import numpy as np
import sys
from sys import argv

import os
import summary
import store_data

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly'] # Removing the .readonly will make enable modifying cal

def main():
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
    
    if argv[1] == 'summary':
        # Not very elegant, try to find a better way to express this        
        if len(sys.argv)  == 2:
            summary.getSummary()
        elif len(sys.argv) == 3:
            summary.getSummary(argv[2])
        elif len(sys.argv) == 4:
            summary.getSummary(argv[2], argv[3])
        elif len(sys.argv) == 5:
            summary.getSummary(argv[2], argv[3], argv[4])            
        elif len(sys.argv) == 6:
            summary.getSummary(argv[2], argv[3], argv[4], argv[5])  

    elif argv[1] == 'store-data':
        if len(sys.argv) == 2:
            store_data.fetchAndStoreData(creds)
        elif len(sys.argv) == 3:
            store_data.fetchAndStoreData(creds, argv[2])

    elif argv[1] == 'updatefrom': 
        store_data.updateData(creds, argv[2])

    elif argv[1] == 'help':
        summary.getHelp()
            
if __name__ == '__main__':
    main()
