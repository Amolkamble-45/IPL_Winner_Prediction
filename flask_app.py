from flask import Flask, render_template, request
import pandas as pd
import pickle

with open('pipe_2.pkl', 'rb') as f:
    model = pickle.load(f)

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
         'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur', 'Chennai',
          'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi',
          'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']

lossprob = "None"
winprob = "None"

app = Flask(__name__)


@app.route('/pred', methods=['POST', 'GET'])
def predict():
    global lossprob, winprob, input_df, predictions, dict_images
    if request.method == 'POST':
        battingteam = request.form['battingteam']
        bowlingteam = request.form['bowlingteam']
        city = request.form['city']
        target = int(request.form['target'])
        score = int(request.form['score'])
        overs = int(request.form['over'])
        wickets = int(request.form['wickets'])
        if 0 <= target <= 300 and overs >= 0 and overs <= 20 and wickets <= 10 and score >= 0:
            # Perform the prediction steps
            print(bowlingteam)
            print(city)

            runs_left = target - score
            balls_left = 120 - (overs * 6)
            wickets = 10 - wickets
            currentrunrate = score / overs
            requiredrunrate = (runs_left * 6) / balls_left

            input_df = pd.DataFrame(
                {'batting_team': [battingteam], 'bowling_team': [bowlingteam], 'city': [city], 'runs_left': [runs_left],
                 'balls_left': [
                     balls_left], 'wickets_left': [wickets], 'total_runs_x': [target], 'cur_run_rate': [currentrunrate],
                 'req_run_rate': [requiredrunrate]})

            dict_images = {
                'Chennai Super Kings': "static/team_logos/CSK-Logo.jpeg",
                'Royal Challengers Bangalore': "static/team_logos/Royal-Challengers-Bangalore.jpeg",
                'Delhi Capitals': "static/team_logos/Delhi-Capitals-logo-1.jpg",
                'Kolkata Knight Riders': "static/team_logos/KKR-logo.jpeg",
                'Mumbai Indians': "static/team_logos/Mumbai-Indians-new-logo.jpeg",
                'Kings XI Punjab': "static/team_logos/Punjab-Kings.jpeg",
                'Rajsthan Royals': "static/team_logos/Rajasthan-Royals-Logo.jpeg",
                'Sunrisers Hydrabad': "static/team_logos/Sunrisers-Hyderabad.jpeg",
                'batting_team': battingteam,
                'bowling_team': bowlingteam
            }

            print(input_df)
            prediction = model.predict_proba(input_df)
            lossprob = prediction[0][0]
            winprob = prediction[0][1]
            predictions = (lossprob, winprob)
            lossprob *= 100
            lossprob = round(lossprob, 2)
            winprob *= 100
            winprob = round(winprob, 2)

            return render_template('result.html', input_df=input_df, lossprob=lossprob, winprob=winprob,
                                   dict_images=dict_images)
        else:
            return "There is something wrong with the input, please fill in the correct details as of IPL T-20 format"


@app.route('/')
def index():
    return render_template('home.html', teams=teams, cities=cities)



if __name__ == '__main__':
    app.run(debug=True)
