import pandas as pd
from flask import Flask, render_template, url_for, send_from_directory, request, redirect, url_for, jsonify
from over_under import load_data, calculate_over_under

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/baseball')
def baseball():
    return render_template('coming_soon.html')

@app.route('/soccer')
def soccer():
    return render_template('coming_soon.html')

@app.route('/hockey')
def hockey():
    return render_template('coming_soon.html')

@app.route('/Team_Information')
def team_information():
    return render_template('coming_soon.html')

@app.route('/About_Us')
def about_us():
    return render_template('coming_soon.html')

@app.route('/Standings')
def standings():
    return render_template('coming_soon.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Add code here to handle signup
        # For now, we will just redirect to the home page
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add code here to handle login
        # For now, we will just redirect to the home page
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/Live_Events')
def live_events():
    return render_template('coming_soon.html')

@app.route('/run_spread', methods=['POST'])
def run_spread():
    # Extract arguments from the request
    spread_favorite_input = float(request.json.get('spread_favorite_input'))
    favorite_team_input = request.json.get('favorite_team_input')
    underdog_input = request.json.get('underdog_input')
    is_team_favorite_home = request.json.get('is_team_favorite_home') == 'yes'

    # Import the calculate_combined_percentage function from Spread.py
    from Spread import calculate_combined_percentage

    # Run the calculate_combined_percentage function with the arguments
    output = calculate_combined_percentage(spread_favorite_input, favorite_team_input, underdog_input, is_team_favorite_home)

    # Return the output
    return jsonify({'output': output})

@app.route('/run_over_under', methods=['POST'])
def run_over_under():
    # Extract arguments from the request
    home_team = request.json.get('home_team')
    your_single_number = float(request.json.get('your_single_number'))

    # Load the data and set the index
    df = pd.read_csv('results_home.csv', index_col='team_home')

    # Run the calculate_over_under function with the arguments
    output = calculate_over_under(home_team, your_single_number, df)

    # Return the output
    return jsonify({'output': output})


if __name__ == '__main__':
    app.run(debug=True)