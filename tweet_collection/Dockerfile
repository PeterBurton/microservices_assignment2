FROM golang:1.8

WORKDIR /app
COPY . .

RUN go get -d ./...
RUN go run collect_publish.go

CMD ["app"]

