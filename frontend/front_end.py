from flask import Flask, render_template
from pymongo import MongoClient
import datetime

# Connect to mongoDB using the service name as the hostname
client = MongoClient("datastore:27017")
db = client.tweet_db
tweet_col = db.tweet_polarities
reddit_col = db.reddit_polarities

app = Flask(__name__)

@app.route("/sentiment")
def hello():
    
    return refresh_page()
    
    
def refresh_page():

    # Query the DB for all the tweet collection results from the last minute
    t_result = list(tweet_col.find({'date':{'$lt':datetime.datetime.utcnow(), '$gt':datetime.datetime.utcnow() - datetime.timedelta(minutes=1)}}))
    
    t_polarity_sum = 0
    t_polarity_count = 0
    
    # Calculate the average polarity and round it to 2 decimal places
    for res in t_result:
        t_polarity_sum = t_polarity_sum + res['polarity']
        t_polarity_count = t_polarity_count + 1
        
    try:
        t_avg_polarity = t_polarity_sum/t_polarity_count
        tweet_rounded_polarity = str("%.2f" % t_avg_polarity)
    except ZeroDivisionError:
        tweet_rounded_polarity = "Zero Division Error"

    # Query the DB for all the reddit collection results from the last minute
    r_result = list(reddit_col.find({'date':{'$lt':datetime.datetime.utcnow(), '$gt':datetime.datetime.utcnow() - datetime.timedelta(minutes=1)}}))
    
    r_polarity_sum = 0
    r_polarity_count = 0
    
    # Calculate the average polarity and round it to 2 decimal places
    for res in r_result:
        r_polarity_sum = r_polarity_sum + res['polarity']
        r_polarity_count = r_polarity_count + 1

    try:    
        r_avg_polarity = r_polarity_sum/r_polarity_count
        reddit_rounded_polarity = str("%.2f" % r_avg_polarity)
    except ZeroDivisionError:
        reddit_rounded_polarity = "Zero Division Error"
    
    # Render the webpage and pass in the result
    return render_template('index.html', result1=tweet_rounded_polarity, result2 = reddit_rounded_polarity)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
