import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'chi': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'new': 'new_york_city.csv',
             'washington': 'washington.csv',
             'was': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
        (str) day - name of the day of week to filter by, or "all"
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:

        print("please choose a city or the first three letters of one")
        print("please note, no gender or YOB data exists for Washington ")
        city = input('chicago, new york city, washington.').lower()
        if city not in CITY_DATA:
            print('It appears that, you have chosen an incorrect city.')
            print('Please choose again, chicago, new york city, washington: ')
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        print("please select a month")
        print("if you select all, no filter will be applied")
        month = input(' january-june, or "all": ').lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month != 'all' and month not in months:
            print('Please enter a full valid month name')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('please select a day of the week')
        print('if you select "all" no filter will be applied')
        day = input('monday-sunday or "all":').lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday']
        if day != 'all' and day not in days:
            print('Please enter a correct day')
        else:
            break

    print('-'*60)
    return city, month, day


def confirm_filters(city, month, day):

    while True:
        print(f"you have selected {city,month,day}")
        confirmation = input("are these filters correct?,y/n: ").lower()
        answers = ['y', 'n']
        if confirmation not in answers:
            confirm_filters(city, month, day)
        if confirmation == ('n'):
            main()
        if confirmation == ('y'):
            break


def load_data(city, month, day):
    """
    Loads data corresponding to filters

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
        (str) day - name of the day of week to filter by, or "all"
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # loading the corresponding csv
    df = pd.read_csv(CITY_DATA[city])

    # Start Time to datetime conversion
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # get month and day of week from the created 'Start Time' column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        # index months ls to retrieve int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    # month filter for new df
        df = df[df['month'] == month]

    # if day filter is used
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def data_output(df):

    x = 0
    print("Would you like to display")
    print("The top 5 rows of data?")
    choice = input('y/n: ').lower()
    pd.set_option('display.max_columns', None)

    while True:
        if choice == 'n':
            break
        print(df[x:x+5])
        choice = input('Would you like the next 5 rows of data y/n:').lower()
        x += 5
        if choice != 'n' or 'y':
            print('please enter a valid choice "y/n"')


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month:', calendar.month_name[most_common_month])

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', most_common_day)

    # display the most common start hour
    # first take hour from 'Start Time'
    df['hour'] = df['Start Time'].dt.hour

    most_common_hour = df['hour'].mode()[0]

    print('Most Common Start Hour:', most_common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displaying most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('Most frequented departure point is:', most_common_start)

    # displaying most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('Most frequent End Station:', most_common_end)

    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station']+" "+"to"+" "+df['End Station']
    combo = df['combo'].mode()[0]
    print(f"The most common departure-end combination is {combo}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    # minute, second conversion.
    minute, second = divmod(travel_time, 60)
    # hour, minutes conversion
    hour, minute = divmod(minute, 60)
    # f string to print hour,minute and seconds.
    print(f" The total travel time is is {hour} hours")
    print(f" {minute} minutes and {second} seconds.")

    # display mean travel time
    mean_time = round(df['Trip Duration'].mean())
    print(f"The average time is {mean_time} minutes")
    print(f"or {mean_time/60} hours")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of User Type:\n', df['User Type'].value_counts())

    # Washington does not have a gender column, so 'if' needed
    if 'Gender' in df:
        print('Counts of Gender:', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth,
    # 'if' needed for Washington
    if 'Birth Year' in df:
        min_year = int(df['Birth Year'].min())
        print('Earliest Year of Birth:', min_year)
        recent_year = int(df['Birth Year'].max())
        print('Most Recent Year of Birth:', recent_year)
        common_year = int(df['Birth Year'].mode()[0])
        print('Most Common Year of Birth:', common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def restart_program():
    restart = input('would you like to restart program y/n: ')
    if restart.lower() == 'y':
        main()
    else:
        print("thank you for taking the time to check out my program:")
        print("to see some of my other projects")
        print("visit my github on <https://github.com/Ron-Chinner> ")
        exit()


def main():
    while True:
        city, month, day = get_filters()
        confirm_filters(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_output(df)
        restart_program()


if __name__ == "__main__":
    main()
