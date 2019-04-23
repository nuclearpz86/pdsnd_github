import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    user_choice1 = str(input('Which city\'s bikeshare data would you like to explore? Chicago, New york, or Washington?\n'))
    city = user_choice1.lower()
    while city not in ['chicago', 'new york', 'washington']:
        print ('Your choice is invalid, please try again')
        user_choice1 = str(input('Please enter Chicago, New york, or Washington.\n'))
        city = user_choice1.lower()
    print('Thank you, you\'ve choosen', city,'!')
    user_choice2 = str(input('Would you like to filter the data by month, day or not at all? Type \'all\' for no filter\n'))
    filter = user_choice2.lower()
    while filter not in ['all', 'month', 'day']:
        print ('Your choice is invalid, please try again')
        user_choice2 = str(input('\nPlease enter all, month, or day.\n'))
        city = user_choice2.lower()
    if filter == 'all':
        month = 'all'
        day = 'all'
    elif filter == 'month':
        user_choice3 = str(input('Which month? January, February, March, April, May, or June?\n'))
        month = user_choice3.lower()
        while month not in months:
            print ('Your choice is invalid, please try again')
            user_choice3 = str(input('Please enter January, February, March, April, May, or June?\n'))
            month = user_choice3.lower()
        day = 'all'
    elif filter == 'day':
        user_choice4 = str(input('Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday.\n'))
        day = user_choice4.lower()
        while day not in days:
            print ('Your choice is invalid, please try again')
            user_choice4 = str(input('Please enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday.\n'))
            day = user_choice4.lower()
        month = 'all'
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month']==month]
    if day != 'all':
        df = df[df['day_of_week']==day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday' ]
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time']=pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    ride_count_month = df['month'].value_counts().values[0]
    df['day'] = df['Start Time'].dt.dayofweek
    popular_day = df['day'].mode()[0]
    ride_count_day = df['day'].value_counts().values[0]
    df['hour'] = df['Start Time'].dt.hour
    popular_hour=df['hour'].mode()[0]
    ride_count_hour = df['hour'].value_counts().values[0]

    if df['month'].unique().size != 1 and df['day'].unique().size != 1:
        print('The most popular month is {} with {} rides!'.format(months[popular_month-1], ride_count_month))
        print('The most popular day of the week is {} with {} rides!'.format(days[popular_day],ride_count_day))
        print('The most popular time of day is {}:00 o\'clock with {} rides!'.format(popular_hour,ride_count_hour))
    elif df['month'].unique().size == 1 and df['day'].unique().size != 1:
        print('In {}, there were total {} rides.'.format(months[popular_month-1],ride_count_month))
        print('The most popular day of the week is {} with {} rides!'.format(days[popular_day], ride_count_day))
        print('The most popular time of day is {}:00 o\'clock with {} rides in {}!'.format(popular_hour, ride_count_hour,months[popular_month-1]))
    elif df['day'].unique().size == 1 and df['month'].unique().size != 1:
        print('{} {}s were the most popular with {} rides, out of {} {} rides!'.format(months[popular_month-1],days[popular_day],ride_count_month,ride_count_day, days[popular_day]))
        print('The most popular time of day is {}:00 o\'clock with {} rides on {}!'.format(popular_hour, ride_count_hour,days[popular_day]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start = df['Start Station'].mode()[0]
    popular_start_count = df['Start Station'].value_counts()[0]
    print('The most popular start station is {} with {} rides.'.format(popular_start,popular_start_count))
    popular_end = df['End Station'].mode()[0]
    popular_end_count=df['End Station'].value_counts()[0]
    print('The most popular end station is {} with {} rides.'.format(popular_end,popular_end_count ))
    df_count=df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'count'})
    max_freq = df_count['count'].max()
    df_count = df_count[df_count['count']==max_freq]
    print('The most frequent combination of start and end stations are:')
    print(df_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#['Start Time', 'End Time', 'Trip Duration', 'Start Station','End Station', 'User Type', 'Gender', 'Birth Year']
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = df['Trip Duration'].sum(skipna=True)
    print('The total travel time is {}.'.format(total_travel_time))
    average_travel_time = df['Trip Duration'].mean()
    converted = str(datetime.timedelta(seconds = average_travel_time))
    print('The average travel time is {} in HH:MM:SS format.'.format(converted))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # if dataframe includes gender and
    if len(df.columns) == 13:
        #gender info
        print(df['Gender'].value_counts())
        #birth year stats
        print('The earilest birth year is {}.'.format(df['Birth Year'].min()))
        print('The most recent birth year is {}.'.format(df['Birth Year'].max()))
        print('The most common birth year is {}.'.format(df['Birth Year'].mode().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_lines(df):
    """Displays the next 5 lines of data until user stop."""
    choice = input('\nWould you like to see individual trip data? Enter yes or no.\n')
    lines = 0
    while choice.lower() not in ['yes', 'no']:
        print('Invalid input.')
        choice = input('Try again. Yes or No')
    while choice.lower() == 'yes':
        print(df.iloc[lines:lines+5,:])
        lines +=5
        choice = input('Would you like to see more? Yes or No\n')
        while choice.lower() not in ['yes', 'no']:
            print('Invalid input.')
            choice = input('Try again.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_lines(df)
        restart = input('Would you like to restart? Enter yes or no.\n')
        while restart.lower() not in['yes','no']:
            print('Invalid input.')
            restart = input('Try again. Yes or No\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
