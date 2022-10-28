package main

import (
	"context"
	"log"
	"math/rand"
	"time"

	qdb "github.com/questdb/go-questdb-client"
)

func main() {
	ctx := context.TODO()
	sender, err := qdb.NewLineSender(
		ctx,
		qdb.WithAddress("localhost:9009"),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer sender.Close()

	var (
		device_types = []string{"blue", "red", "green", "yellow"}
	)

	iter := 1000
	batch := 1000

	ts := 1
	delay_ms := 50

	min_lat := 19.50139
	max_lat := 64.85694
	min_lon := -161.75583
	max_lon := -68.01197

	for it := 0; it < iter; it++ {
		for i := 0; i < batch; i++ {
			t := time.Now()
			err = sender.
				Table("ilp_test").
				Symbol("device_type", device_types[rand.Intn(len(device_types))]).
				Int64Column("duration_ms", int64(rand.Intn(4000))).
				Float64Column("lat", rand.Float64()*(max_lat-min_lat)).
				Float64Column("lon", rand.Float64()*(max_lon-min_lon)).
				Int64Column("measure1", int64(rand.Int31())).
				Int64Column("measure2", int64(rand.Int31())).
				Int64Column("speed", int64(rand.Intn(100))).
				At(ctx, t.UnixNano())
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
