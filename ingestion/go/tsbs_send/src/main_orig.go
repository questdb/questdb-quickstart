package main

import (
	"context"
	"log"
	"math/rand"
	"time"
	"os"

	qdb "github.com/questdb/go-questdb-client"
)

func getEnv(key, fallback string) string {
    if value, ok := os.LookupEnv(key); ok {
        return value
    }
    return fallback
}

func getBoolEnv(key string) bool {
	if value, ok := os.LookupEnv(key); ok {
		return (value == "TRUE" || value == "True" || value == "true" || value == "1" || value == "t")
	}
	return false
}

func main() {
	opts := make([]qdb.LineSenderOption, 0, 4)

	host := getEnv("QDB_CLIENT_HOST", "localhost")
	port := getEnv("QDB_CLIENT_PORT", "9009")
	opts = append(opts, qdb.WithAddress(host + ":" + port) )

	auth_kid := getEnv("QDB_CLIENT_AUTH_KID","")
	auth_d := getEnv("QDB_CLIENT_AUTH_D","")
	log.Printf("kid %s d %s ", auth_kid, auth_d)
    if (auth_kid != "" && auth_d != "") {
		log.Printf("kid %s d %s ", auth_kid, auth_d)
		opts = append(opts, qdb.WithAuth(auth_kid, auth_d))
	}

	if getBoolEnv("QDB_CLIENT_TLS") {
		log.Printf("with TLS")
		opts = append(opts, qdb.WithTls())
	}

	ctx := context.TODO()
	sender, err := qdb.NewLineSender(
		ctx,
		opts...
	)
	if err != nil {
		log.Fatal(err)
	}
	defer sender.Close()

	var (
		device_types = []string{"blue", "red", "green", "yellow"}
	)

	iter := 10000
	batch := 100

	ts := 1
	delay_ms := 500

	min_lat := 19.50139
	max_lat := 64.85694
	min_lon := -161.75583
	max_lon := -68.01197

	for it := 0; it < iter; it++ {
		for i := 0; i < batch; i++ {
			//t := time.Now()
			err = sender.
				Table("ilp_test").
				Symbol("device_type", device_types[rand.Intn(len(device_types))]).
				Int64Column("duration_ms", int64(rand.Intn(4000))).
				Float64Column("lat", rand.Float64()*(max_lat-min_lat)).
				Float64Column("lon", rand.Float64()*(max_lon-min_lon)).
				Int64Column("measure1", int64(rand.Int31())).
				Int64Column("measure2", int64(rand.Int31())).
				Int64Column("speed", int64(rand.Intn(100))).
				AtNow(ctx)
				//At(ctx, t.UnixNano())
			if err != nil {
				log.Fatal(err)
			}
			ts += 1
		}
		err = sender.Flush(ctx)
		if err != nil {
			log.Fatal(err)
		}
		wrote := int64(batch)
		log.Printf("wrote %d rows", wrote)

		if delay_ms > 0 {
			log.Printf("sleeping %d milliseconds", delay_ms)
			time.Sleep(time.Duration(delay_ms) * time.Millisecond)
		}
	}
	log.Printf("Summary: %d rows sent", iter*batch)
}
