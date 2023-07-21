# syntax=docker/dockerfile:1
FROM golang:1.20-alpine
RUN apk --no-cache add curl
WORKDIR /app
COPY go.mod ./
RUN go mod download
RUN go mod download github.com/questdb/go-questdb-client
COPY src/*.go ./
CMD while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' host.docker.internal:19003)" != "200" ]]; do sleep 1; done;go run main_orig.go
