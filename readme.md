# Google Calendar Enhancer 

###### Why pay for google calendar time insights when you can get the same functionality for free?

This app enhances Google Calendar by adding functionality to help plan your days/weeks/months. For instance, using the app, you can quickly get information about how much time you've spent/are going to spend doing certain activities during a specific timeframe.

## Functionality

Currently, the program has three useable commands: **store-data**, **summary**, and **help**.

### store-data
When ```store-data``` is called, it stores your google calendar events from the specified calendar. If called alone, it fetches and stores calendar events between a specified date (2022-08-29 by default, can be changed at ```/store_data/storeData.py```) to the current day.

Alternatively, one can pass a second argument, which should be a date in "yyyy-mm-dd" format. In such an event, it fetches data between the default from_date to the given date. Below is an example that fetches data between 2022-08-29 to 2022-11-07

```
cl store-data 2022-11-07
```

### summary
```summary``` can be run without arguments, which returns a current-day summary. Alternatively, it can be given 1-3 additional arguments:

- [activity]
    - Can be - in which case default activities are returned.
    - Replace - with the activity of interest to only fetch information about that specific activity.

- [timespan]
    - Can be year/month/week/day 
    - The default arg is "date", filtering the df by dates

- [specificity]
    - By default, it fetches the current date. 
    - Can be given a value of **total**, which provides total hours for specified activities.
    - Can be given a week/year/day/date, e.g., 45 (week), giving total hours spent on that period

##### Example line of code:
- Returns total hours spent on a list of pre-specified activities, which can be changed from ```/summary/getData.py```

```
cl summary - week total
```

### help
Returns information about the other commands.



## Installation
For the program to work, you must download a google API key and fetch data from your calendar. [work in progress, details about this will be posted later]

To run this program via terminal in Linux, you need to make changes to your .bashrc file.

#### Open .bashrc

```
$ vim ~/.bashrc
```

#### Add the alias
Ubuntu has a default command called cal, so I went with the alias "cl." Make the alias go to the google-calendar-enhancer working directory, and then run main.py.

```
alias cl='cd /home/lauri/programming/google-calendar-enhancer/ && python main.py
```

#### Et voilà! Now you can run the program from your terminal
For example, to get your events for this day, write the following:

```
cl summary
```



### Future update ideas

- Improve functionality of the store-data command:
    - For example, make it possible to alter the default from_date
    - Enable storing data by typing a week, month, etc., and taking the last day of the specified timeframe.
    - Refrain from overriding the (possibly) existing database each time the command is run.
- Add data analytics 
- ColorId categorization:
    - This would enable more imaginative names for activities and more exciting insights in the long run. I haven't added this functionality yet, because for some reason, google calendars default activity color doesn't have a colorId, and I am greatly fond of the default color.
- Improve error handling. At the moment, the program will throw cryptic messages to unsuspecting users.