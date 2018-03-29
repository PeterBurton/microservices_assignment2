import pika
from textblob import TextBlob
from pymongo import MongoClient
import datetime

#rmq_uri = os.getenv('RMQ_URI')
#appended_uri = "amqp://guest:guest@" + rmq_uri
#mongo_uri = os.getenv("DATASTORE_ADDR")
#app_mongo_uri = "mongodb://" + mongo_uri

client = MongoClient("datastore:27017")
db = client.tweet_db
col = db.polarities

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel() 
channel.queue_declare(queue='tweets')
print('********Waiting for tweets. Press CTRL+C to exit********')

def callback(ch, method, properties, body):
    
    # We pass each tweet to TextBlob for decoding
    tweet = TextBlob(body.decode("utf-8"))
    
    # Use Textblob to attempt to correct any mis-spelt words 
    # to try and make analysis more accurate
    tweet.correct()
    
    result = {}
    result["date"] = datetime.datetime.utcnow()
    result["polarity"] = tweet.sentiment.polarity
    
    col.insert_one(result)

channel.basic_consume(callback,
                      queue='tweets',
                      no_ack=True)

channel.start_consuming()