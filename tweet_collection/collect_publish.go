package main

// Import all required packages
import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/dghubble/go-twitter/twitter"
	"github.com/dghubble/oauth1"
	"github.com/streadway/amqp"
)

func failOnError(err error, msg string) {
	// Log any errors
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {

	// Connect to rabbitMQ using the docker service name as the host name
	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	// Declare a queue named 'tweets'
	q, err := ch.QueueDeclare(
		"tweets", // name
		false,    // durable
		false,    // delete when unused
		false,    // exclusive
		false,    // no-wait
		nil,      // arguments
	)
	failOnError(err, "Failed to declare a queue")

	// Configure httpClient with secrets/keys/tokens etc.
	config := oauth1.NewConfig("zHi6YhB0zmqCd3nyHYqlcF1zc", "GWUHuhwGWS3OCrsEsmvL2BBnJtOap8knDfMQrsNpUmWwS3tgNC")
	token := oauth1.NewToken("3067657355-gPeu5FJODLSIKf5spHpthxZhNGd3NQYB2ZWGAds", "Ow1HObvQMPTseNeGrO3aoQuAmrY9ranbNPgUz5u65RbEB")
	httpClient := config.Client(oauth1.NoContext, token)

	// initialise Twitter Client
	client := twitter.NewClient(httpClient)

	// Demux the twitter stream, grab the body of the text that we're interested in
	demux := twitter.NewSwitchDemux()
	demux.Tweet = func(tweet *twitter.Tweet) {
		body := "TWEET " + tweet.Text
		err = ch.Publish(
			"",     // exchange
			q.Name, // routing key
			false,  // mandatory
			false,  // immediate
			amqp.Publishing{
				ContentType: "text/plain",
				Body:        []byte(body),
			})
		failOnError(err, "Failed to publish a message")
	}

	fmt.Println("Starting Stream...")

	// Set the client to filter for a search term, in this case 'trump'
	filterParams := &twitter.StreamFilterParams{
		Track:         []string{"Trump"},
		StallWarnings: twitter.Bool(true),
	}
	stream, err := client.Streams.Filter(filterParams)
	if err != nil {
		log.Fatal(err)
	}

	// Receive messages until stopped or stream quits
	go demux.HandleChan(stream.Messages)

	// Wait for SIGINT and SIGTERM (HIT CTRL-C)
	ch1 := make(chan os.Signal)
	signal.Notify(ch1, syscall.SIGINT, syscall.SIGTERM)
	log.Println(<-ch1)

	fmt.Println("Stopping Stream...")
	stream.Stop()
}
