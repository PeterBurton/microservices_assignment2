import pika
from textblob import TextBlob
from pymongo import MongoClient
import datetime

# Connect to mongoDB using the service name as the hostname
client = MongoClient("datastore:27017")
db = client.tweet_db
col = db.polarities

# Connect to rabbitMQ with pika, using a blocking connection. Had to specify heartbeat due to issues with rabbitMQ disconnecting pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat_interval=0))
channel = connection.channel() 
# Declare the message queue we want to use
channel.queue_declare(queue='tweets')
print('********Waiting for tweets. Press CTRL+C to exit********')

def callback(ch, method, properties, body):
    
    # We pass each tweet to TextBlob for decoding
    tweet = TextBlob(body.decode("utf-8"))
    
    # Use Textblob to attempt to correct any mis-spelt words 
    # to try and make analysis more accurate
    tweet.correct()
    
    # Get the timestamp and the polarity 
    result = {}
    result["date"] = datetime.datetime.utcnow()
    result["polarity"] = tweet.sentiment.polarity
    
    # Insert into collection
    col.insert_one(result)

channel.basic_consume(callback,
                      queue='tweets',
                      no_ack=True)

channel.start_consuming()
