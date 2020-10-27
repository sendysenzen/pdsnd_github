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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    month = None
    day = None
    
    while True : 
        try :
            city = str(input("Please enter the city (chicago/new york city/washington) : \n"))
        except ValueError:
            print('Sorry, you have to type in string') 
            continue
        if city.lower() not in ('chicago','new york city','washington') : 
            print('You did not type the correct city')
            continue
        else :
            city = city.lower()
            print('\n you chose city : \n',city)
            break
                         
    # get user input for month (all, january, february, ... , june)
    while True : 
        try :
            month = str(input("Please enter the month correctly (from January to June, or All ): \n"))
        except ValueError:
            print('Sorry, you have to type in string') 
            continue
        if month.title() not in ('January','February','March','April','May','June','All') : 
            print('You did not type the correct month')
            continue
        else :
            month = month.title()
            print('\n you chose month : \n',month) 
            break
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True : 
        try :
            day = str(input("Please enter the day correctly (from Monday to Sunday, or All ): \n"))
        except ValueError:
            print('Sorry, you have to type in string') 
            continue
        if day.title() not in ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All') : 
            print('You did not type the correct day')
            continue
        else : 
            day = day.title()
            print('\n you chose day : \n',day)
            break

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
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month and day - if applicable
    if month != 'All' and day != 'All':
        df = df[(df['month'] == month) & (df['day_of_week'] == day)]
    elif month != 'All' and day == 'All' :
        df = df[df['month'] == month]
    elif month == 'All' and day != 'All' :
        df = df[df['day_of_week'] == day]
    elif month == 'All' and day == 'All': 
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['hour'] = df['Start Time'].dt.hour
        df['month'] = df['Start Time'].dt.month_name()
        df['day_of_week'] = df['Start Time'].dt.day_name()
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('the most common month : \n', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('the most common day : \n', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('the most common start hour : \n', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('the most common used start station : \n', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('the most common used end station : \n', common_end)

    # display most frequent combination of start station and end station trip
    common_combi = df.groupby(['Start Station','End Station']).size().idxmax()
    print('the most common combination start and end station : \n', common_combi)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('total travel time : \n', total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('average travel time : \n', mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user = df['User Type'].value_counts()
    print('total counts of user type \n', count_user)

    # Display counts of gender
    try :
        count_gender = df['Gender'].value_counts()
        print('total counts of gender \n', count_gender)

    # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('The earliest year of birth : \n',earliest)
        print('the most recent year of birth : \n', recent)
        print('the most common year of birth : \n', common_birth)
    except KeyError : 
        print("No data Gender / Birth Year available")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_row(df):
    """" Display some raw data """
    #Asking to input how many raw lines data to be seen
    numrow = 0
    rawdata = input('Do you want to see some raw data? (yes/no)').lower()
        
    if rawdata not in ('yes','no') : 
        print('\n You didnt type correctly')
    elif rawdata == 'yes':     
        while True :
            try:
                numrow = int(input('\nHow many raw data lines do you want to display? \n'))
            except ValueError:
                print('Sorry, you have to type a number')

            #Display number of lines
            numrow = int(numrow)
            print('You choose to display ',numrow ,' data lines \n \n')
            print(df.iloc[0:numrow,:],'\n')

            df3 = df.iloc[0:numrow,:]
            #Display Summary for better information data analysis
            print('\n\n-----SUMMARY for ',numrow,'raw data lines-----\n')
            print('Average travel time for ',numrow,'lines : ',df3['Trip Duration'].mean())
            print('The longest travel time : ',df3['Trip Duration'].max())
            print('The shortest travel time :',df3['Trip Duration'].min())

            again=input('\n Do you want to see another sets of raw data again? (yes/no)').lower()
            if again == 'no' :
                break
            elif again not in ('yes','no') :
                print('\n You didnt type correctly')
                break 
            
    elif rawdata == 'no':
        return  

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_row(df)
              
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    
