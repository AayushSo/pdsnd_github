# Exploring Bikeshare Data of Motivate (Udacity Project)

### Date created
Created on 18th of April, 2024

### Project Title
Interactive Bike Share Stats Tracker 

### Description	
The aim of this project is to analyze bike data of the company Motivate and print relevant stats for the user to see.
The user should be able to filer the data as per requirements:

- City (Required)
- Filter by Month (optional, default 'all')
- Filter by day of week (optional, default 'all')

The filtered data needs to be analyzed to see the below observations:
- Popular times of travel (i.e., occurs most often in the start time)
	- most common month
	- most common day of week
	- most common hour of day

- Popular stations and trip
	- most common start station
	- most common end station
	- most common trip from start to end (i.e., most frequent combination of start station and end station)

- Trip duration
	- total travel time
	- average travel time

- User info
	- counts of each user type
	- counts of each gender (only available for NYC and Chicago)
	- earliest, most recent, most common year of birth (only available for NYC and Chicago)
	
Project template used from Udacity Course downloads

### Files used
bikeshare.py
chicago.csv
washington.csv
new_york_city.csv
CSV files are derived from Motivate co. via Udacity. Thanks!

### Usage
File can be run in console as
`python bikeshare.py`

User needs to input the following text (in **bold**)
`
Display log info? y/n : *y*
INFO: libraries loaded... successfully
Welcome to Motivate Co Archives. What would you like to view today?
Current data available is for Chicago, New York City and Washington. Which city data to load?
*chicago*
INFO: Chicago database loaded successfully
Do you want to filter data by a specific month? If so please enter month to filter by. Else type 'all' : january
INFO: Selected month is :  *january*
Do you want to filter data by a specific day of the week? If so please enter day to filter by. Else type 'all' : wednesday
INFO: Selected day of week is :  *wednesday*
INFO: User data inputs loaded successfully.
...
_Stats_Displayed_Here_
...
Total rows of data available are 3389 rows
Do you wish to view raw data? y/n : y
Displaying records 1-5 out of 3389
     Unnamed: 0          Start Time            End Time  Trip Duration                 Start Station                     End Station   User Type Gender  Birth Year  month  dow  hour
...
Continue? y/n : *n*
----------------------------------------
Would you like to view other stats? Enter y/n : *n*
`
Display of log info can be enabled or disabled using (y,n) respectively.
Cities input must be (New York City,NYC,Washington,Chicago)
Months must be standard gregorian months (January, February, etc.). Numbers 1 through 12 can also be given as input.
Day of week must be (Monday, Tuesday, etc.). Numbers 0-6 for Monday to Sunday respectively can also be given as input. 