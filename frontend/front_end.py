from flask import Flask, render_template
from pymongo import MongoClient
import datetime

#mongo_uri = os.getenv("DATASTORE_ADDR")
#app_mongo_uri = "mongodb://" + mongo_uri

client = MongoClient("datastore:27017")
db = client.tweet_db
collection = db.polarities

app = Flask(__name__)

@app.route("/sentiment")
def hello():
    
    return refresh_page()
    
    
def refresh_page():
    
    result = list(collection.find({'date':{'$lt':datetime.datetime.utcnow(), '$gt':datetime.datetime.utcnow() - datetime.timedelta(minutes=1)}}))
    
    polarity_sum = 0
    polarity_count = 0
    
    for res in result:
        polarity_sum = polarity_sum + res['polarity']
        polarity_count = polarity_count + 1
        
    avg_polarity = polarity_sum/polarity_count
    
    rounded_polarity = str("%.2f" % avg_polarity)
    
    return render_template('index.html', result=rounded_polarity)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
