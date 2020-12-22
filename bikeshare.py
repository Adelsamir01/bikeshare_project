import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


MONTH_DATA = ['all', 'jan', 'feb', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']

def get_filters():
   
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("which city do you want analyzed? (chicago, new york city, washington)\n").lower()
    while(city!='chicago' and city !='new york city' and city!='washington'):
        print(city, " is not a correct city! Please choose from (chicago, new york city, washington) ")
        city = input().lower()
        

    month_name = ''
    while month_name.lower() not in MONTH_DATA:
        month_name = input("Please Enter the month: (all, Jan, Feb, March, April, May, June)\n")
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
        else:
            #error  finding the month in the list so we ask the user to input again 
            print("Please Enter the correct month: (all, Jan, Feb, March, April, May, June)\n")

    # Getting the day from the user
    day_name = ''
    while day_name.lower() not in DAY_DATA:
        day_name = input("\nEnter the day (all, sunday, monday, ..)\n")
        if day_name.lower() in DAY_DATA:
            day = day_name.lower()
        else:
            #error  finding the day in the list so we ask the user to input again 
            print("Please enter the correct day (all, sunday, monday, ..)\n")



    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        
         if day != 'all':
        # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    return df

def display_raw_data(df):
    
    i = 0
    raw = input("Do you wanna display five rows of the data? (Yes/No)\n").lower()
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        print(df[i:i+5])
        raw = input("Do you wanna display another five rows of the data? (Yes/No)\n").lower()
        i += 5

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    MCM = df['month'].mode()[0]
    print("Most Common Month: ", MCM)

    MCD = df['day_of_week'].mode()[0]
    print("Most Common Day of the Week: ", MCD)

    df['hour'] = df['Start Time'].dt.hour
    
    MCSH = df['hour'].mode()[0]

    print('Most Popular Start Hour:', MCSH)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    MCUSS = df['Start Station'].mode()[0]
    print("Most Commonly Used Start Station: ", MCUSS)
    

    MCUES = df['End Station'].mode()[0]
    print("Most Commonly Used End Station: ", MCUES)

    df['Start_End_Comp'] = df['Start Station'] +' and '+ df['End Station']
    most_freq_start_end = df['Start_End_Comp'].mode()[0]
    print("most frequent combination of start station and end station trip: ", most_freq_start_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    print("Total Travel Time: ", total_time/(60), "Hours")

    mean_time = df['Trip Duration'].mean()
    print("Mean Travel Time: ", mean_time, "Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)

    try:
        
        gender_types = df['Gender'].value_counts()
        print(gender_types)
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        
        print("Earliest Year of Birth: ", earliest)
        print("Most Recent Year of Birth: ", most_recent)
        print("Most Common Year of Birth: ",most_common_year)
    except:
        print("\nThis City Has no Gender Stats or Birth Stats\n")

    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
