from confluent_kafka import Consumer, KafkaException
import pandas as pd

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address

    
    'group.id': 'my_group',  # Consumer group id
    'auto.offset.reset': 'earliest'
}

# Create Consumer instance
consumer = Consumer(**conf)

# Subscribe to topic
topic = 'my_topic2'
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print('%% %s [%d] reached end at offset %d\n' %
                      (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            # Proper message
            # result = msg.value().to_csv('Names', decoding='utf-8')
            # print("-----", result)
            print('Received message: {} [{}] at offset {} with key {}'.format(msg.value().decode('utf-8'), msg.topic(), msg.offset(), msg.key().decode('utf-8')))
            df = msg.value().decode('utf-8').split('\n')
            records = []
            print(df)
            for i in df:
                records.append(','.join(i.split()))
            print(records)
            dataFrame = msg.value()
            print("\nvalue:::", dataFrame[0])

except KeyboardInterrupt:
    pass
finally:
    # Close down consumer to commit final offsets.
    consumer.close()
