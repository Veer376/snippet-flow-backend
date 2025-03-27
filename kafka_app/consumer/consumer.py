import os
from confluent_kafka import Consumer, KafkaError
import requests
import json 

BROKER = os.getenv("BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = "new-snippet"

conf = {
        'bootstrap.servers': BROKER,
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    }

consumer = Consumer(conf)
consumer.subscribe([TOPIC])

def consume(msg):
    """
    Send snippet to FastAPI using an HTTP request
    """
    print('inside the consume function')
    


try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            print("up and running...", flush=True)
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("End of partition reached.")
            else:
                print(f"Consumer error: {msg.error()}")
            continue
        requests.post("http://fastapi:8000/snippet/consume", json=json.loads(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    print("Shutting down consumer...")


# async def consume(snippet: dict):
#     """
#     Send snippet to FastAPI using an async HTTP request
#     """
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             "http://fastapi:8000/snippet/consume",
#             json=snippet,
#             timeout=10.0
#         )
#         return response.json()
