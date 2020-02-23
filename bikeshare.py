import time
import pandas as pd
import numpy as np
from bikeshare_input import user_input as ui

selected_city = ""

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global selected_city
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ui.prompt("Please enter a city name to analyze the data ({}): ".format(", ".join(map(lambda c:c.title(),ui.CITY_DATA.keys()))), str, "city")

    # get user input for month (all, january, february, ... , june)
    month = ui.prompt("Please enter a month to filter the data ({}). Enter all to include all months: ".format(", ".join(map(lambda m: m.title(), ui.MONTH_DATA))), str, "month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ui.prompt("Please enter a day of the week to filter the data ({}). Enter all to inlcude all days of the week: ".format(", ".join(map(lambda d: d.title(), ui.DAY_OF_THE_WEEK_DATA))), str, "day")

    print('-'*150)    
    selected_city = city
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
    df = pd.read_csv(ui.CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int        
        month = ui.MONTH_DATA.index(month.lower()) + 1        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"The most common month is: {df['month'].mode()[0]}\n")

    # display the most common day of week
    print(f"The most common day of the week is: {df['day_of_week'].mode()[0]}\n")

    # display the most common start hour
    print(f"The most common start hour is: {df['Start Time'].dt.hour.mode()[0]}\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"The most commonly used start station is: {df['Start Station'].mode()[0]}\n")

    # display most commonly used end station
    print(f"The most commonly used end station is: {df['End Station'].mode()[0]}\n")

    # display most frequent combination of start station and end station trip
    combo = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print(f"The most frequent combination of start station and end station trip is: {combo.index[0]} - {combo.max()} times.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"Total travel time: {df['Trip Duration'].sum()}\n")

    # display mean travel time
    print(f"Mean travel time: {df['Trip Duration'].mean()}\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    if( 'User Type' in df.columns):
        print(f"Counts of user types:\n{df['User Type'].value_counts()}\n")
    else:
        print(f'The Dataset for city {selected_city} doesn\'t have User Type values')

    # Display counts of gender
    if( 'Gender' in df.columns):
        print(f"Counts of Gender types:\n{df['Gender'].value_counts()}\n")
    else:
        print(f'The Dataset for city {selected_city} doesn\'t have Gender values')

    # Display earliest, most recent, and most common year of birth
    if( 'Birth Year' in df.columns):
        print(f"The earliest year of birth: {int(df['Birth Year'].min())}\n") 
        print(f"The most recent year of birth: {int(df['Birth Year'].max())}\n") 
        print(f"The most common year of birth: {int(df['Birth Year'].mode()[0])}\n") 
    else:
        print(f'The Dataset for city {selected_city} doesn\'t have Birth Year values')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def print_raw_data(df):
    """ Displays 5 lines of raw data from the dataframe """
    offset = 0
    msg = ""
    while True:
        if(offset > 0):
            msg = " the next"
        show_raw_data = ui.prompt(f"Do you want to see{msg} 5 lines of raw data? Enter yes or no.\n",str)
        if(show_raw_data.lower() == 'yes'):            
            print(df.iloc[offset: offset+5])
            offset += 5
            continue
        elif (show_raw_data.lower() == 'no'):
            break
        else:
            print("Please enter a valid response yes or no.\n")

def main():    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)
       
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
