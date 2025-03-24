from confluent_kafka import AdminClient, NewTopic

BROKER = "kafka:9092"  # Change to your Kafka broker address
TOPIC = "new-snippet"         # Change to your desired topic name

admin_client = AdminClient({"bootstrap.servers": BROKER})

topic = NewTopic(TOPIC, num_partitions=1, replication_factor=1)
admin_client.create_topics([topic])

print(f"Topic {TOPIC} created")