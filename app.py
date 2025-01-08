from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
pipe = pickle.load(open('pipe.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form data
    data = request.form
    batting_team = data['batting_team']
    bowling_team = data['bowling_team']
    city = data['city']
    current_score = int(data['current_score'])
    overs = float(data['overs'])
    wickets = int(data['wickets'])
    last_five = int(data['last_five'])

    # Derived features
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = current_score / overs

    # Create input DataFrame for prediction
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city],
        'curr_score': [current_score],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'crr': [crr],
        'last_five': [last_five]
    })

    # Make prediction
    prediction = pipe.predict(input_df)[0]

    # Render the result on a new page
    return render_template('result2.html', predicted_score=int(prediction))

if __name__ == '__main__':
    app.run(debug=True)
