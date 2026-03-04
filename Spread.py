import pandas as pd

breadScores = pd.read_csv('breadScores.csv')

def calculate_combined_percentage(spread_favorite_input, favorite_team_input, underdog_input, is_team_favorite_home):
    breadScores = pd.read_csv('breadScores.csv')

    # Function to create a subset based on spread_favorite range and print percentages
    def print_team_favorite_cover_spread_percentage():
        # Create a subset based on spread_favorite range
        subset = breadScores[(breadScores['spread_favorite'] >= spread_favorite_input - 1.0) & (breadScores['spread_favorite'] <= spread_favorite_input + 1.0)]

        # Check if the subset is not empty
        if not subset.empty:
            team_favorite_counts = subset['team_favorite_id'].value_counts()
            matching_counts = subset[subset['team_favorite_id'] == subset['winner_against_spread']]['team_favorite_id'].value_counts()

            percentages = pd.DataFrame({
                'Percentage': (matching_counts / team_favorite_counts).round(2)
            })

            # Add a column for spread range
            percentages['Spread_Range'] = f"Subset: {spread_favorite_input - 1.0} to {spread_favorite_input + 1.0}"

            return percentages
        else:
            print("No data found for the specified spread_favorite. Returning an empty DataFrame.")
            return pd.DataFrame()

    # Call the function and get the percentage for the team_favorite_id
    result_team_favorite = print_team_favorite_cover_spread_percentage()
    percentage1 = result_team_favorite[result_team_favorite['Spread_Range'] == f"Subset: {spread_favorite_input - 1.0} to {spread_favorite_input + 1.0}"]['Percentage'].values[0]


    # Helper function to calculate team percentages
    def calculate_team_percentage(team_data, is_home_team, opponent_team):
        filtered_data = team_data[team_data['team_away' if is_home_team else 'team_home'] == opponent_team]

        if len(filtered_data) == 0 or overall_percentages_df.loc[overall_percentages_df['Team'] == opponent_team, 'Overall_Percentage'].values[0] == 0:
            percentage = overall_percentages_df.loc[overall_percentages_df['Team'] == opponent_team, 'Overall_Percentage'].values[0]
        else:
            team_percentage = sum((filtered_data['team_favorite_id'] == favorite_team_input) &
                                   (filtered_data['team_favorite_id'] == filtered_data['winner_against_spread'])) / len(filtered_data)

            percentage = round(team_percentage, 2) if team_percentage != 0 else overall_percentages_df.loc[overall_percentages_df['Team'] == opponent_team, 'Overall_Percentage'].values[0]

        return percentage

    # List of teams to analyze
    teams_of_interest = [
        "San Francisco 49ers", "New York Jets", "Chicago Bears",
        "Cincinnati Bengals", "Cleveland Browns", "Los Angeles Rams",
        "Green Bay Packers", "Dallas Cowboys", "Indianapolis Colts",
        "Miami Dolphins", "Las Vegas Raiders", "Tampa Bay Buccaneers",
        "Tennessee Titans", "Washington Commanders", "Pittsburgh Steelers",
        "Atlanta Falcons", "Carolina Panthers", "Kansas City Chiefs",
        "Minnesota Vikings", "Seattle Seahawks", "Philadelphia Eagles",
        "Los Angeles Chargers", "New Orleans Saints", "Denver Broncos",
        "New England Patriots", "New York Giants", "Buffalo Bills",
        "Jacksonville Jaguars", "Arizona Cardinals", "Detroit Lions",
        "Houston Texans", "Baltimore Ravens"
    ]

    # Create a list to store overall percentages
    overall_percentages = []

    # Iterate over each team
    for team in teams_of_interest:
        # Filter data for the current team
        team_data = breadScores[(breadScores['team_favorite_id'] == team)]

        # Calculate the overall percentage and round to 2 decimal places
        overall_percentage = round((team_data['team_favorite_id'] == team_data['winner_against_spread']).mean(), 2)

        # Append results to the overall_percentages list
        overall_percentages.append({
            'Team': team,
            'Overall_Percentage': overall_percentage
        })

    # Create a DataFrame from the list
    overall_percentages_df = pd.DataFrame(overall_percentages)

    # Create a list to store overall percentages
    # Filter data for the current team
    team_data = breadScores[(breadScores['team_favorite_id'] == favorite_team_input)]

    # Calculate the percentage based on whether the favorite team is the home or away team
    if is_team_favorite_home:
        filtered_data = team_data[(team_data['team_home'] == favorite_team_input) & (team_data['team_away'] == underdog_input)]
    else:
        filtered_data = team_data[(team_data['team_away'] == favorite_team_input) & (team_data['team_home'] == underdog_input)]

    # Calculate percentage2
    percentage2 = calculate_team_percentage(filtered_data, is_team_favorite_home, underdog_input)

    # Calculate the combined percentage
    combined_percentage = percentage1 * percentage2

    # Output the result in a sentence
    return f"{favorite_team_input} has a {combined_percentage * 100}% chance to cover a spread of {spread_favorite_input} against {underdog_input}"