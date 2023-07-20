package io.questdb.samples.ilp_ingestion;

import io.questdb.client.Sender;

import java.util.Random;


public class IlpSender {
    static final String[] deviceTypes = {"blue", "red", "green", "yellow"};
    static final Double min_lat = 19.50139, max_lat = 64.85694, min_lon = -161.75583, max_lon = -68.01197;

    public static void main(String[] args) {
        Random random = new Random();
        int max_items = 1000000, batch = 100, delay_ms = 500;

        try (Sender sender = Sender.builder()
                .address("localhost:9009")
                .build()) {

            for (int i = 1; i <= max_items; i++) {
                sender.table("ilp_test")
                        .symbol("device_type", deviceTypes[random.nextInt(deviceTypes.length)])
                        .longColumn("duration_ms", random.nextInt(4000))
                        .doubleColumn("lat", random.nextDouble() * (max_lat - min_lat))
                        .doubleColumn("lon", random.nextDouble() * (max_lon - min_lon))
                        .longColumn("measure1", random.nextInt(Integer.MAX_VALUE))
                        .longColumn("measure2", random.nextInt(Integer.MAX_VALUE))
                        .longColumn("speed", random.nextInt(100))
                        .atNow();
                if (i % batch == 0) {
                    sender.flush();
                    Thread.sleep(delay_ms);
                }
            }

        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
