FROM golang:1.8

WORKDIR /go/src/app
COPY . .

RUN go get -d ./...
RUN go install ./...

CMD ["go","run","collect_publish.go"]

