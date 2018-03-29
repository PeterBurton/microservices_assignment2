# Use golang 1.8 as the parent image
FROM golang:1.8

# Set the working directory to /go/src/app
WORKDIR /go/src/app

# Copy the current directory contents into the container at /go/src/app
COPY . .

# Download and install all required dependencies
RUN go get -d ./...
RUN go install ./...

# Run collect_publish.go when the container launches
CMD ["go","run","collect_publish.go"]

