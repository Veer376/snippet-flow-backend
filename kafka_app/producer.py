from confluent_kafka import Producer
import json 
import os 

BROKER = os.getenv("BOOTSTRAP_SERVERS", "kafka:9092")

producer = Producer({"bootstrap.servers": BROKER})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")


def produce_message(topic, value):
    try: 
        producer.produce(
            topic=topic,
            value=json.dumps(value).encode('utf-8'),
            callback=delivery_report
        )
        producer.poll(0) # wait for message deliveries
        producer.flush() # wait for all messages to be delivered hello
        print(f"\nValue: '{value}' \nTopic '{topic}'")
    except Exception as e:
        print(f"An error occurred: {e}")
    

