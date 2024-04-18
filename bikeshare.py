'''
Author : Aayush Soni
Date : 16th of April 2024

The aim of this project is to analyze bike data of the company Motivate and print relevant stats for the user to see.
The user should be able to filer the data as per requirements:
	1. City (Required)
	2. Filter by Month (optional, default 'all')
	3. Filter by day of week (optional, default 'all')

The filtered data needs to be analyzed to see the below observations:
#1 Popular times of travel (i.e., occurs most often in the start time)
	most common month
	most common day of week
	most common hour of day

#2 Popular stations and trip
	most common start station
	most common end station
	most common trip from start to end (i.e., most frequent combination of start station and end station)

#3 Trip duration
	total travel time
	average travel time

#4 User info
	counts of each user type
	counts of each gender (only available for NYC and Chicago)
	earliest, most recent, most common year of birth (only available for NYC and Chicago)
	
Project template used from Udacity Course downloads
'''

logger=False # Use this to enable/disable log messages
inp=input("Display log info? y/n : ")
if len(inp)==0 : logger=False #Default disable in case of no text
elif inp.lower()[0]=='y' : logger=True


def logparse(*args):
	""" 
	TODO: dump logs to a file.
	For now is a 'pass' so user does not see logs on console
	"""
	pass

if logger : log=print
else : log=logparse

#############################################################
### LIBRARY LOADING
#############################################################
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
scipy_loader=False
try : from scipy import stats; scipy_loader=True
except : 
	log("Warning: scipy library not found")
	

log("INFO: libraries loaded... successfully")

#############################################################
### Local functions and global variables
#############################################################

cities= { 'chicago': 'chicago.csv','nyc': 'new_york_city.csv','new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
days=['monday','tuesday','wednesday','thurdsay','friday','saturday','sunday','all']
months = ['all','january', 'february', 'march', 'april', 'may', 'june', 'july','august','september','october','november','december']

def get_user_input():
	"""Get user filters"""
	
	invalid_ctr=0 #max retries is hard coded as 5
	
	#Enter the city
	city=""
	while not city in cities :
		city = input("Current data available is for Chicago, New York City and Washington. Which city data to load? \n")
		city = city.strip().lower()
		if not city in cities :
			invalid_ctr+=1
			log(f"Error :city {city} not present in database")
			if not logger : print(f"Looks like Motivate hasn't reached your city, "+city+" yet!")
			if invalid_ctr >=5 :
				log("Error: Unknown input: ",city)
				exit()
	df=pd.read_csv(cities[city])
	log(f'INFO: {city.title()} database loaded successfully')
	
	# convert time data tie datetime format
	df['Start Time']=df['Start Time'].astype('datetime64[ns]')
	df['End Time']=df['End Time'].astype('datetime64[ns]') 
	
	#remove NAN rows
	df=df.dropna()
	
	#add cols for month, day of week, hour of day
	df['month']=df['Start Time'].dt.month
	df['dow']=df['Start Time'].dt.day_of_week
	df['hour']=df['Start Time'].dt.hour
	month_filter=False
	dow_filter=False
	
	#Enter the month
	month=""
	while not month in months :
		month=input("Do you want to filter data by a specific month? If so please enter month to filter by. Else type 'all' : ")
		if len(month)==0 : month='all' #Default null option
		month = month.strip().lower()
		if month.isdigit():
			month=int(month)
			if month>0 and month <=12 : month=months[month]
			else : 
				log("Error : invalid month range. Please use 1-12 for Jan - Dec")
				invalid_ctr+=1
				if invalid_ctr >=5 :
					log("Error: Unknown input: ",month)
					exit("Max retries reached! Exiting...")
		if not month in months :
			invalid_ctr+=1
			log("Error : Invalid month")
			if invalid_ctr >=5 :
				log("Error: Unknown input: ",month)
				exit("Max retries reached! Exiting...")
	log("INFO: Selected month is : ",month)
	if not month=='all' :
		df=df[df['month']==months.index(month)]
		month_filter=True
	#Enter the dow
	dow=""
	while not dow in days :
		dow=input("Do you want to filter data by a specific day of the week? If so please enter day to filter by. Else type 'all' : ")
		if len(dow)==0 : dow='all' #Default null option
		dow = dow.strip().lower()
		if dow.isdigit() :
			dow=int(dow)
			if dow<7 : dow=days[dow]
			else :
				log("Error : invalid day range. Please use 0-7 for Mon - Sun")
				invalid_ctr+=1
				if invalid_ctr >=5 :
					log("Error: Unknown input: ",dow)
					exit("Max retries reached! Exiting...")
		if not dow in days :
			invalid_ctr+=1
			log("Error : Invalid day value")
			if not logger : print("Invalid day value. Please enter monday-sunday (or) 0-6 ")
			if invalid_ctr >=5 :
				log("Error: Unknown input: ",dow)
				exit("Max retries reached! Exiting...")
	log("INFO: Selected day of week is : ",dow)
	if not dow=='all' :
		df=df[df['dow']==days.index(dow)]
		dow_filter=True
	
	return df,city,month,dow,month_filter,dow_filter

def time_stats(df,month,dow,month_filter=False,dow_filter=False):
	"""Displays statistics on the most frequent times of travel."""
	
	print('\nCalculating The Most Frequent Times of Travel...\n')
	start_time = time.time()
	
	# display the most common month
	if not month_filter:
		print("The most popular month of travel is ",end='')
		print(months[df['month'].value_counts().idxmax()].title())
	
	# display the most common day of week
	if not dow_filter:
		print("The most popular day of travel is ",end='')
		print(days[df['dow'].value_counts().idxmax()].title())
	
	# display the most common start hour
	print("The most popular hour of travel","" if not month_filter else " in "+month.title(),
											"" if not dow_filter else " on "+dow.title()  ," is ",end='')
	hour_of_day = int(df['hour'].value_counts().idxmax())
	if hour_of_day > 12 : print( hour_of_day - 12, " PM")
	elif hour_of_day==0 : print("12 AM")
	else : print(hour_of_day," AM")
	
	
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""
	
	print('\nCalculating The Most Popular Stations and Trip...\n')
	start_time = time.time()
	
	# display most commonly used start station
	most_pop_start=df['Start Station'].value_counts().idxmax()
	print("Most populous starting station is : ", most_pop_start) 
	
	# display most commonly used end station
	most_pop_end=df['End Station'].value_counts().idxmax()
	print("Most populous end station is : ", most_pop_end) 
	
	# display most frequent combination of start station and end station trip
	a,b=df.groupby(['Start Station','End Station']).size().idxmax()
	print(f"Most popular route to travel is from '{a}' to '{b}'")
	
	#print(f"Average (mean) time of this trip is {df.loc[df['Start Station']==a].loc[df['End Station']==b]['Trip Duration'].mean()}s")
	sec2week("Average (mean) time of this trip is",df.loc[df['Start Station']==a].loc[df['End Station']==b]['Trip Duration'].mean())
	if a != most_pop_start and b !=most_pop_end   :
		print("Neither is the start station of this route the most popular starting station, nor is the end station the most popular stop station. The programmer finds irony in this.")
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def trip_duration_stats(df,filter_trip_cnt=10):
	"""Displays statistics on the total and average trip duration."""

	print('\nCalculating Trip Duration...\n')
	start_time = time.time()
	
	# display total travel time
	tot_sec=df['Trip Duration'].sum()
	sec2week("Total trip duration is ",tot_sec)
	# display mean travel time
	tot_sec=df['Trip Duration'].mean()
	sec2week("Average (mean) trip duration is ",tot_sec)
	
	### other trip stats
	#Sample routes by variation in trip times
	df1=df.groupby(['Start Station','End Station']).filter(lambda x: len(x)>filter_trip_cnt) # remove routes with <10 occurrences
	if len(df1)==0 : df1=df # no route has <10 occurrences, just consume all routes
	x=df1.groupby(['Start Station','End Station'])['Trip Duration']	# group by start and end station
	y=x.std()/x.mean() #find standard deviation. normalize with mean so we can compare routes of differing lengths
	y.dropna(inplace=True) #remove NAN
	if scipy_loader : y=y[(np.abs(stats.zscore(y)) < 3)] # looks like there are a lot of outliers that are probably negative data that wrap around to v high values ?!? filtering out extreme values to only select accurate data
	else : log("Warning: outliers not filtered")
	print(f"Route with max variation is (start stn,end stn) : {y.idxmax()} with std/mean = {y.max()}")
	print(f"Route with min variation is (start stn,end stn) : {y.idxmin()} with std/mean = {y.min()}")
	(y*100).hist(bins=5)
	plt.xlabel("Variation in route duration(%)")
	plt.ylabel("Number of routes")
	plt.show()
	#Sample routes by average trip times
	y=x.mean() #find standard deviation. normalize with mean so we can compare routes of differing lengths
	if scipy_loader : y=y[(np.abs(stats.zscore(y)) < 3)] 
	print(f"Route with highest average duration is (start stn,end stn) : {y.idxmax()} with mean duration = {y.max()}s")
	print(f"Route with lowest average duration is (start stn,end stn) : {y.idxmin()} with mean duration = {y.min()}s")
	sec2week("Mean route duration is ",y.mean())
	sec2week("Std in route duration is ",y.std())
	(y/60).hist(bins=100)
	plt.xlabel("Average route duration (minutes)")
	plt.ylabel("Number of routes")
	plt.show()
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def user_stats(df):
	"""Displays statistics on bikeshare users."""

	print('\nCalculating User Stats...\n')
	start_time = time.time()

	# Display counts of user types
	print("User Types and Stats:")
	print(df.groupby('User Type').size())	
	print()

	# Display counts of gender
	if 'Gender' in df.columns:
		print("Gender count:")
		print(df.groupby('Gender').size(),end='\n\n')
		df2=pd.DataFrame({'Female':df[df['Gender']=='Female'].groupby(['hour'])['Trip Duration'].sum() ,
							'Male':df[df['Gender']=='Male'].groupby(['hour'])['Trip Duration'].sum()})
		print(f"Correlation between male and female trip durations by month is {df2.corr().loc['Female']['Male']}")
		f_to_m_perc=round(df2['Female'].mean()/df2['Male'].mean()*100 *100)/100 #round percentage to 2 places od decimal
		print(f"Number of trips drive by women is {f_to_m_perc} % of trips drivem by men ")
		#print()
	else : print("Gender stats not available for current selection",end='\n\n')

	# Display earliest, most recent, and most common year of birth
	if 'Birth Year' in df.columns:
		print("DOB stats:")
		print(f"Earliest year of birth is    : {df['Birth Year'].min()}")
		print(f"Most recent year of birth is : {df['Birth Year'].max()}")
		print(f"Most common year of birth is : {df['Birth Year'].mode()[0]}")
		print(f"Most trips are taken by users with year of birth : { df.groupby('Birth Year')['Trip Duration'].count().idxmax()}")
		df.groupby('Birth Year')['Trip Duration'].count().plot()
		plt.ylabel("Number of trips taken")
		plt.show()
	else : print("DOB stats not available for current selection")

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)

def df_chunker(df,size=5):
	"""Iterator to return chunks of dataframe in chunks of 'size'"""
	for i in range(0,len(df),size):
		yield df.iloc[i:i+size]

def display_data(df,size=5):
	"""Display rows of filtered csv data"""
	print(f"Total rows of data available are {len(df)} rows")
	inp=input("Do you wish to view raw data? y/n : ")
	if inp.lower()[0]=='y':
		tmp=0
		for rowdat in df_chunker(df,size):
			print(f'Displaying records {tmp+1}-{min(tmp+size,len(df))} out of {len(df)}')
			print(rowdat)
			tmp+=size
			if(tmp>=len(df)) : continue
			inp=input("Continue? y/n : ")
			if len(inp)==0 : continue # just press enter to continue, for the lazy
			if inp.lower()[0]=='n': return 0
		return 0
	else : 
		print("Affirmitive not detected. Skipping viewing of data...")
		return 0

def sec2week(init_str,tot_sec):
	"""Get week:day:hour:mis:sec from seconds, and print it based on init_str"""
	tot_min,tot_sec=divmod(tot_sec,60)
	tot_hour,tot_min=divmod(tot_min,60)
	tot_day,tot_hour=divmod(tot_hour,60)
	tot_week,tot_day=divmod(tot_day,60)
	weekstr= str(int(tot_week)) + ' weeks,' if tot_week >0 else ''
	daystr=str(int(tot_day)) + ' days,' if tot_day >0 or tot_week >0 else ''
	hrstr=str(int(tot_hour)) + ' hr,' if tot_hour >0 or tot_day >0 or tot_week >0 else ''
	minstr=str(int(tot_min)) + ' min,' if tot_min >0 or tot_hour >0 or tot_day >0 or tot_week >0 else ''
	secstr=str(int(tot_sec)) + ' s' if tot_sec >0 or tot_min >0 or tot_hour >0 or tot_day >0 or tot_week >0 else ''
	print(f"{init_str}{weekstr} {daystr} {hrstr} {minstr} {secstr} ")
	
#############################################################
### Main function
#############################################################


while __name__ == '__main__':
	try:
		print("Welcome to Motivate Co Archives. What would you like to view today?")
		df,city,month,dow,month_filter,dow_filter=get_user_input()
		log("INFO: User data inputs loaded successfully.")
		print('-'*40)
		print(f'Displaying statistics of {city.title()}', f'for {month.title()}' if month_filter else '', f'on {dow.title()} ' if dow_filter else '')
		#print("I am here")
		if df.size==0:
			print("Oops! No data available. Please choose different constraints.")
		else:
			time_stats(df,month,dow,month_filter,dow_filter)
			station_stats(df)
			trip_duration_stats(df,filter_trip_cnt=10)#when we group by routes, how many routes do we remove, i.e. remove entries if the route is traveled < 'filter_trip_cnt' times
			user_stats(df)
			_=display_data(df)
		print('-'*40)
		go_again=input("Would you like to view other stats? Enter y/n : ")
		while len(go_again)==0 :go_again=input("Would you like to view other stats? Enter y/n : ")
		print()
		if go_again.lower()[0]=='n' : log("INFO: Exiting based on user input."); exit()
		
	except (EOFError,KeyboardInterrupt) :
		log("Error : Detected Ctrl-Z. Exiting...")
		exit()