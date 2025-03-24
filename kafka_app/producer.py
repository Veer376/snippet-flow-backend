from confluent_kafka import Producer

BROKER = "kafka:9092"

producer = Producer({"bootstrap.servers": BROKER})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


def produce_message(topic, key, value):
    try: 
        producer.produce(
            topic=topic,
            key=str(key).encode('utf-8'),
            value=str(value).encode('utf-8'),
            callback=delivery_report
        )
        producer.poll(0)
        producer.flush()
        print(f"Message: {key} : {value} produced to the {topic}")
    except Exception as e:
        print(f"An error occurred: {e}")
    

