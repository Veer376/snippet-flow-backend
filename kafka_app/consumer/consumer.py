from confluent_kafka.admin import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'  # start from the earliest message
}

consumer = Consumer(conf)

consumer.subscribe(["new-snippet"])

while True:
    msg = consumer.poll(1.0) 
    if msg is None: continue
    if msg.error():
        print(f"Error: {msg.error()}")
        continue
    print(f"Received message: key={msg.key()}, value={msg.value()}")

            
