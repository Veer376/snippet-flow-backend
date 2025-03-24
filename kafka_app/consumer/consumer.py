import os
from confluent_kafka import Consumer, KafkaError

# BROKER = os.getenv("BOOTSTRAP_SERVERS", "kafka:9092")
BROKER = "kafka:9092"
TOPIC = "new-snippet"

conf = {
        'bootstrap.servers': BROKER,
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    }

consumer = Consumer(conf)
consumer.subscribe([TOPIC])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            print("Waiting for message or error in poll()", flush=True)
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("End of partition reached.")
            else:
                print(f"Consumer error: {msg.error()}")
            continue
        print(f"Received message: {msg.value().decode('utf-8')} (key={msg.key()})")
except KeyboardInterrupt:
    print("Shutting down consumer...")

