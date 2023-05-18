import pandas as pd

def get_snotel_df():
    df = pd.read_csv('../content/csv/seasonal_snotel_mean.csv')
    df = df.set_index('Date')
    return df

def get_danger_df(area='West Slopes South', drop_no_rating=True):
    df = pd.read_csv('../content/csv/danger_ratings.csv')
    if drop_no_rating:
        df = df[df['Danger Rating'] != 'NO RATING']
    df = df[(df == area).any(axis=1)]
    df['Danger Rating'] = df['Danger Rating'].map({ 'NO RATING': 0, 'LOW': 1, 'MODERATE': 2, 'CONSIDERABLE': 3, 'HIGH': 4, 'EXTREME': 5 })
    try:
        df = df['Date'] = pd.to_datetime(df['Date'], format='%b %D %Y')
    except Exception as err:
        print('Cant format date')

    df = df.set_index('Date')
    return df