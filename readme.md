
This app is used for enhancing the Google Calendar by adding some functionality to help 
planning your days/weeks/months. For instance, using the app you can quickly get information 
about how much time you've spent / are going to spend doing certain activities during a certain timeframe. 




===========================================BRAINSTORMING===========================================
For some reason the default blue color doesn't have a color id, so that's a bit tricky. 

=====COLUMNS=====
YEAR WEEK DAY DATE ACTION START END DURATION UGLYSTART UGLYEND
-> Could add weekday?

=====Database operations=====
- Need a function that fetches the data from point X to this date, and writes a dataframe.
- Need a function that fetches data for a certain time period

Group related functionality together
--> folders such as:
- api
- utils/logic
- database

SHOULD BE ABLE TO FETCH DATABASE LIKE:
DATE CATEGORY HOURS

