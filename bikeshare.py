import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    print('\nHello! Let\'s explore some US bikeshare data!\n')
    print('You can currently explore 3 cities: Chicago, New York City and Washington!')
   
    while True:
            # Ask user for input and validates the user input. 
            city = input('\nPlease type your preferred city.\n').lower()
            validate_city = ['chicago' ,'new york city', 'washington']

            if city not in validate_city:
                print('Oops! Please check your spelling.')
                continue
            else:
                print('\nIt seems you would like to explore data for {}\n'.format(city))
                break

    while True:
             # Ask user for input and validates the user input.  
            month = input('\nWhich month would you like to filter the data?. (january, february, ....., june.). Type "all" to select all months.\n').lower()
            validate_month = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

            if month not in validate_month:
                print('Oops! Please check your spelling.')
                continue
            else:
                break

    while True:
             # Ask user for input and validates the user input.  
            day = input('\nWhich day would you like to filter the data?. (eg. sunday). Type "all" to filter by week.\n').lower()
            validate_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

            if day not in validate_day:
                print('Oops! Please check your spelling.')
                continue
            else:
                break
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # load the files into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time columns to a datetime 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # create month and day column from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filters by month or by all months 
    if month != 'all':

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1 

        df = df[df['month']==month]
    # filters by day or all of the week
    if day != 'all':
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculates the most frequent month of travel
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    freq_month = df['month'].mode()[0]
    print('The most common month: ',freq_month)
        

    # Calculates the most frequent day of travel
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    freq_day = df['day_of_week'].mode()[0]
    print('The most common day: ',freq_day)

   # Calculates the most frequent hour of travel
    freq_start_hr = df['hour'].mode()[0]
    print('The most common start hour: ', freq_start_hr)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculates the most frequently used start station
    freq_start_station = df['Start Station'].mode()[0]
    print('Most commonly used end station: ',freq_start_station)

    # Calculates the most frequently used end station
    freq_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ',freq_end_station)

    # Calculates the most frequent combination of start station and end station trip
    freq_comb_SE = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent combination of Start and End Station: ', freq_comb_SE)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculates the the total trip duration based on filter
    total_tt = df['Trip Duration'].sum()
    print('Total travel time: ',total_tt)

   # Calculates the the total trip duration based on filter
    mean_tt = df['Trip Duration'].mean()
    print('Mean travel time', mean_tt)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts the type of users per the filter
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Counts the Gender per the filter
    print(' ')
    while True:
        try:
            gender = df['Gender'].value_counts()
        except KeyError:
            print('Gender')
            print('Sorry!. There is no available information.')
        else:
            print(gender)
        break
        
    # filter the first birth year
    print(' ')
    while True:
        try:
            earliest_min = int(df['Birth Year'].min())
        except KeyError:
            print('Birth Year')
            print('Sorry!. There is no available information.')
        else:
            print('Earliest Birth Year', earliest_min)
        break

    # filter the last birth year
    while True:
        try:
            earliest_max = int(df['Birth Year'].max())
        except KeyError:
            print('')
        else:
            print('Most recent Birth year', earliest_max)
        break

    # filter the most common birth year
    while True:
        try:
            cmon_yob = int(df['Birth Year'].mode()[0])
        except KeyError:
            print('')
        else:
            print('Most common year of birth', cmon_yob)
        break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # Ask the user to view data. 
        while True:

            user_input = input('\n Would you like to take a look at the data?. Please type "yes" or "no".\n').lower()
            if user_input == "yes":
                print('{} city bikeshare data preview'.format(city), df.head(5))
                
                # Ask the user to see more data. 
                while True:

                    inc_user_input = input('\nWould you like to see more data?. Please type "yes" or "no".\n').lower()
                    if inc_user_input == "yes":
                        df_head = int(input('\nEnter the number of rows you would like to see. Please enter an integer!. eg. 10.\n'))
                        print('{} city bikeshare data preview'.format(city), df.head(df_head))
            
                    elif inc_user_input == "no":
                        break
                                    
            elif user_input =='no':
                break
            break

        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
