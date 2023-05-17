package io.questdb.samples.ilp_ingestion;

import io.questdb.client.Sender;

import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;


public class IlpCryptoSender {
    static final double MAX_PRICE = 21000.0, MIN_PRICE = 1200.0;
    static final String[] venues = {"CBS", "FUS", "LMX", "BTS"}, sides = {"BUY", "SELL"},
            instruments = {"ETH-USD", "BTC-USD"};

    public static void main(String[] args) {
        Random random = new Random();
        int max_items = 100000, batch = 100, delay_ms = 500;

        double price = ThreadLocalRandom.current().nextDouble(11000, 15000);
        try (Sender sender = Sender.builder()
                .address("localhost:9009")
                .build()) {

            for (int i = 1; i <= max_items; i++) {
                price += ThreadLocalRandom.current().nextDouble(-0.11, 0.11);
                if (price >= MAX_PRICE) {
                    price = MAX_PRICE;
                } else if (price <= MIN_PRICE) {
                    price = MIN_PRICE;
                }

                sender.table("prices")
                        .symbol("venue", venues[random.nextInt(venues.length)])
                        .symbol("instrument_key", instruments[random.nextInt(instruments.length)])
                        .symbol("side", sides[random.nextInt(sides.length)])
                        .doubleColumn("qty", ThreadLocalRandom.current().nextDouble(2800))
                        .doubleColumn("price", price)
                        .atNow();
               if (i % batch == 0) {
                    sender.flush();
                    System.out.println("total rows written so far: " + i);
                   Thread.sleep(delay_ms);

                }
            }

        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
