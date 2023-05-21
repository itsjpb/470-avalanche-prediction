"""
The purpose of this file was to make it so that function definitions
didn't clutter up the notebook file, but because of the way Jupyter
loads this, I'm not really sure if it helps
"""

import calendar
from os import listdir
from os.path import isfile, join
import pandas as pd

def get_snotel_df(file='../content/csv/snotel/new_datasets/1012_new_metrics.csv'):
    df = pd.read_csv(file, comment='#')
    df = df.set_index('Date')
    # Rename the columns to be the same as listed below
    df.columns.values[0] = 'Max Air Temp 24hr'
    df.columns.values[1] = 'Total Snowfall 24hr'
    df.columns.values[2] = 'Min Temp Diff 48hr'
    df.columns.values[3] = 'Delta SWE 24hr'
    
    return df

def get_danger_df(area='West Slopes South', drop_no_rating=True):
    def transform_date(date_string):
        parts = date_string.split(' ')
        month = parts[0]
        day = parts[1]
        year = parts[2]

        day = '0' + day if len(day) < 2 else day
        month = list(calendar.month_abbr).index(month)
        month = '0' + str(month) if month < 10 else month
        return f'{year}-{month}-{day}'

    df = pd.read_csv('../content/csv/danger_ratings.csv')
    if drop_no_rating:
        df = df[df['Danger Rating'] != 'NO RATING']
    df = df[(df == area).any(axis=1)]
    df['Danger Rating'] = df['Danger Rating'].map({ 'NO RATING': 0, 'LOW': 1, 'MODERATE': 2, 'CONSIDERABLE': 3, 'HIGH': 4, 'EXTREME': 5 })
    try:
        df['Date'] = df['Date'].apply(transform_date) # 2022-11-01
    except Exception as err:
        print('Cant format date:', err)

    df = df.set_index('Date')
    return df

def get_training_df():
    snotel_df = get_snotel_df()
    danger_df = get_danger_df()
    
    def init_training_df():
        cols = [ 
            'Max Air Temp 24hr', 
            'Max Air Temp 72hr', 
            'Total Snowfall 24hr', 
            'Total Snowfall 72hr', 
            'Max Windspeed 24hr',
            'Weighted Snowfall 96hr',
            'Min Temp Diff 48hr',
            'Was Heavy Snowfall 24hr',
            'Was High Winds 24hr',
            'Sum Max Temp 72hr',
            'Delta SWE 24hr',
            'Yesterday Danger',
            'Danger Rating'
        ]
        return pd.DataFrame([], columns=cols)
    
    # Set up the correct columns
    df = init_training_df()
    # For every danger rating value
    for idx, row in danger_df.iterrows():
        date = idx
        # Compute the metrics for that date
        
        # Add them to a row and add that row to the dataframe
        df.loc[date] = [0,0,0,0,0,0,0,0,0,0,0,0,0]

    return df

def take_snotel_df_and_calculate_columns(df):
    """Using raw SNOTEL data, calculate the above columns and return them as a dataframe"""

    # Add the column placeholders to the dataframe (or initialize a new one); initialize as null for now
    # String shorthand
    max_temp_72 = 'Max Air Temp 72hr'
    tot_snow_72 = 'Total Snowfall 72hr'
    wgt_snow_72 = 'Weighted Snowfall 96hr'
    was_hvys_24 = 'Was Heavy Snowfall 24hr'
    sum_mtmp_72 = 'Sum Max Temp 72hr'
    df[max_temp_72] = 0 # None
    df[tot_snow_72] = 0 # None
    df[wgt_snow_72] = 0 # None
    df[was_hvys_24] = 0 # None
    df[sum_mtmp_72] = 0 # None

    # Calculate the above metrics
    one_day_ago = None # This wouldn't be necessary if I wasn't indexing on date
    two_days_ago = None
    three_days_ago = None
    for idx, day in df.iterrows():
        df.at[idx, was_hvys_24] = 1 if day['Total Snowfall 24hr'] >= 12 else 0 # todo: update threshold
        if two_days_ago is not None:
            df.at[idx, max_temp_72] = max(
                day['Max Air Temp 24hr'], 
                one_day_ago['Max Air Temp 24hr'], 
                two_days_ago['Max Air Temp 24hr'])
            df.at[idx, tot_snow_72] = \
                day['Total Snowfall 24hr'] \
                + one_day_ago['Total Snowfall 24hr'] \
                + two_days_ago['Total Snowfall 24hr']
            df.at[idx, sum_mtmp_72] = \
                day['Max Air Temp 24hr'] \
                + one_day_ago['Max Air Temp 24hr'] \
                + two_days_ago['Max Air Temp 24hr'] 
        if three_days_ago is not None:
            df.at[idx, 'Weighted Snowfall 96hr'] = \
                day['Total Snowfall 24hr'] * 1.0 \
                + one_day_ago['Total Snowfall 24hr'] * 0.75 \
                + two_days_ago['Total Snowfall 24hr'] * 0.5 \
                + three_days_ago['Total Snowfall 24hr'] * 0.25

        # Update past day placeholders
        three_days_ago = two_days_ago
        two_days_ago = one_day_ago
        one_day_ago = day
    
    # Return the new/updated dataframe
    return df

def get_concat_snotel():
     # Load the 4 snotel datasets with extra columns created as above
    path = '../content/csv/snotel/new_datasets/'
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    dataframes = [get_snotel_df(file=f) for f in files]
    formatted = [take_snotel_df_and_calculate_columns(df) for df in dataframes]

    # Combine them and get the average of all numerical values
    concat = pd.concat(formatted).groupby(level=0)

    return concat

def snotel_datasets_combined_mean(concat=get_concat_snotel()):
    """Calculate columns for all SNOTEL datasets as above and aggregate them using their average"""
    return concat.mean()

def snotel_datasets_combined_median(concat=get_concat_snotel()):
    """Calculate columns for all SNOTEL datasets as above and aggregate them using their median"""
    return concat.median()

def snotel_datasets_combined_max(concat=get_concat_snotel()):
    """Calculate columns for all SNOTEL datasets as above and aggregate them using their maximum"""
    return concat.max()
