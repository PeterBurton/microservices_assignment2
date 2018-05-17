import praw
import pika

#Set up connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='tweets')

#Get a connection to Reddit
reddit = praw.Reddit(client_id='jRkYVufRfKtg2Q',
                     client_secret='jO3eeMhSiTJVE8wPkqq7G4e17pQ', password='microservices18',
                     user_agent='microservices', username='R00038147')

#We want the news subreddit as this should update quite often
subreddit = reddit.subreddit('news')


for comment in subreddit.stream.comments():
    try:
        my_string = "REDDIT " + comment.body
        channel.basic_publish(exchange='',
                      routing_key='tweets',
                      body=my_string)
    except praw.exceptions.PRAWException as e:
        print("There's something wrong Ted!")
        pass
    #print("[*]message sent")

connection.close()