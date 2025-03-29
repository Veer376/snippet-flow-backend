import os
from confluent_kafka import Consumer, KafkaError
import aiohttp
import asyncio
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

async def trigger(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://fastapi:8000/snippet/consume", json=data) as response:
            return response.status

async def consume_messages():
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

        retry = 2
        while retry > 0:
            try:
                data = json.loads(msg.value().decode('utf-8'))
                status = await trigger(data)
                if status == 200:
                    break
                else:
                    print(f"Failed to process message, status code: {status}")
                    retry -= 1
            except Exception as e:
                print(f"Error processing message: {e}")
                retry -= 1

try:
    asyncio.run(consume_messages()) # to start the top level asyncio function
except KeyboardInterrupt:
    print("Shutting down consumer...")
    consumer.close()
