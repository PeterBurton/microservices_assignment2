import pika
from textblob import TextBlob
from pymongo import MongoClient
import datetime

# Connect to mongoDB using the service name as the hostname
client = MongoClient("datastore:27017")
db = client.tweet_db
tweet_col = db.tweet_polarities
reddit_col = db.reddit_polarities

# Connect to rabbitMQ with pika, using a blocking connection. Had to specify heartbeat due to issues with rabbitMQ disconnecting pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel() 
# Declare the message queue we want to use
channel.queue_declare(queue='tweets')
print('********Waiting for tweets. Press CTRL+C to exit********')

def callback(ch, method, properties, body):
    
    # We pass each tweet/reddit comment to TextBlob for decoding
    message = TextBlob(body.decode("utf-8"))

    #Figure out whether it's a tweet or a reddit comment
    message_type = message.split()[:1]
    #print("***********" + message_type[0] + "***********")

    
    # Get the timestamp and the polarity 
    result = {}
    result["date"] = datetime.datetime.utcnow()
    result["polarity"] = message.sentiment.polarity
    
    if message_type[0] == 'REDDIT':
        # Insert into tweet collection
        reddit_col.insert_one(result)
    else:
        #insert into reddit collection
        tweet_col.insert_one(result)
    
channel.basic_consume(callback,
                      queue='tweets',
                      no_ack=True)

channel.start_consuming()
