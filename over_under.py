import pandas as pd

def load_data(csv_path='results_home.csv'):
    df = pd.read_csv(csv_path)
    print(df.head())
    return df

def calculate_over_under(home_team, your_single_number, df):
    # Ensure the columns are treated as intervals
    df.columns = pd.IntervalIndex.from_arrays(
        left=df.columns.str.extract(r'(\d+)', expand=False).astype(float),
        right=df.columns.str.extract(r',\s*(\d+)', expand=False).astype(float),
        closed='left'
    )

    # Find the interval that contains the given number
    over_under_range_for_single_number = df.columns[df.columns.contains(your_single_number)]

    if not over_under_range_for_single_number.empty:
        try:
            column_name = over_under_range_for_single_number[0]
            percent = df.loc[home_team, column_name]
            return f'The over has a {percent:.2f}% chance.'
        except KeyError:
            return f'No data found for {home_team} with {your_single_number} in the calculated range.'
    else:
        return f'No range found for {your_single_number}.'
