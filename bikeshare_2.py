import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input("Would you like to see data for Chicago, New York City, or Washington?\n")
    while city.lower() not in ["chicago", "new york city", "washington"]:
        city=input("\nOoops, invalid option. Would you like to see data for Chicago, New York City or Washington?\n")

    # get user input for filter options
    filtertype=input("Would you like to filter the data by month, day, or not at all? Choose only one option:\n")
    while filtertype.lower() not in ["month", "day", "not at all"]:
        filtertype=input("\nOoops, invalid option. Would you like to filter the data by month, day, or not at all? Choose only one option:\n")

    if filtertype=="month":
        # get user input for month (all, january, february, ... , june)
        month=input("Please enter a month (January, February, ... or June):\n")
        while month.lower() not in ["january", 'february', 'march', 'april', 'may', 'june']:
            month=input("\nOoops, invalid option. Please enter a month (January, February, ... or June):\n")

        day="all"

    elif filtertype=="day":
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day=input("Please enter a day of week (Monday, Tuesday, ... or Sunday):\n")
        while day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day=input("\nOoops, invalid option. Please enter a day of week (Monday, Tuesday, ... or Sunday):\n")

        month="all"

    else:
        day="all"
        month="all"

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
      df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month-1].title()

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print("The most commom month of travel is {}."
          "\nThe most commom day of travel is {}."
          "\nThe most commom starting hour is {}h.".format(popular_month, popular_day, popular_hour))

    print("\nThis took %s seconds." % round(time.time() - start_time,1))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Trip Points'] = df['Start Station'] + " to " + df['End Station']
    popular_trip = df['Trip Points'].mode()[0]

    print("The most commonly used start station was {}."
          "\nThe most commonly used end station was {}."
          "\nThe most commonly combination of start and end station was from {}.".format(popular_start, popular_end, popular_trip))

    print("\nThis took %s seconds." % round(time.time() - start_time,1))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
      df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel= df['Trip Duration'].sum()

    # display mean travel time
    mean_travel= df['Trip Duration'].mean()

    print("The total travel time was {} seconds."
          "\nThe mean travel time was {} seconds.".format(round(total_travel), round(mean_travel)))

    print("\nThis took %s seconds." % round(time.time() - start_time,1))
    print('-'*40)

def user_stats(df, city):

    """Displays statistics on bikeshare users.
    Args:
      df - Pandas DataFrame containing city data filtered by month and day
      (str) city - name of the city to analyze
    """

    print('\nCalculating user stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    for i in user_types:
        print("The number of {}s users is {}.".format(user_types.index[i], user_types[i]))


    if city.lower() != "washington":

        # Display counts of gender
        gender = df['Gender'].value_counts()
        for i in gender:
            print("The number of {} users' is {}.".format(gender.index[i], gender[i]))

        # Display earliest, most recent, and most common year of birth
        earliest_yob=int(df['Birth Year'].min())
        recent_yob=int(df['Birth Year'].max())
        commom_yob=int(df['Birth Year'].mode())

        print("\nThe earliest year of birth is {}."
              "\nThe most recent year of birth is {}."
              "\nThe most common year of birth is {}.".format(earliest_yob, recent_yob, commom_yob))

    print("\nThis took %s seconds." % round(time.time() - start_time,1))
    print('-'*40)

def raw_data(df):
    """
    Asks user if they want to see the raw dataset.
    Args:
     df - Pandas DataFrame containing city data filtered by month and day
    """

    # get user input to check if they want to see the raw data
    rawdata=input("Would you like to see raw data? Enter yes or no.\n")
    while rawdata.lower() not in ["yes", "no"]:
        rawdata=input("\nOoops, invalid option. Would you like to see raw data? Enter yes or no.\n")

    if rawdata=="yes":
        seq=list(range(0, len(df.index)+1, 5))
        for i in range(len(seq)-1):
            print(df[seq[i]:seq[i+1]])
            morerows=input("Would you like to see 5 more rows? Enter yes or no.\n")
            while morerows.lower() not in ["yes", "no"]:
                morerows=input("\nOoops, invalid option. Would you like to see 5 more rows? Enter yes or no.\n")
            if morerows!="yes":
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in ["yes", "no"]:
            restart=input('\nOoops, invalid option. Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
