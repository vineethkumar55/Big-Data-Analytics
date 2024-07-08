import json
from confluent_kafka import Producer
import sys
import xml.etree.ElementTree as ET
import pandas as pd


# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092'  # Kafka broker address
}

# Create Producer instance
producer = Producer(**conf)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Topic
topic = 'my_topic2'
# Example usage
csv_file_path = 'data.csv'
json_file_path = 'Weather_data.json'
xml_file_path = 'data.xml'
keys = ['_id', 'name', 'exposure', 'model']

def read_csv(file_path, keys):
    df = pd.read_csv(file_path)
    filtered_df = df[keys]
    return filtered_df

# def read_json(file_path, keys):
#     with open(file_path, 'r') as f:
#         data = json.load(f)
#     filtered_data = [{key: item.get(key, None) for key in keys} for item in data]
#     df = pd.DataFrame(filtered_data)
#     return filtered_data
def read_json(file_path, keys):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        data = json.load(f)
    filtered_data = [{key: item.get(key, None) for key in keys} for item in data]
    df = pd.DataFrame(filtered_data)
    return filtered_data

def read_xml(file_path, keys):
    tree = ET.parse(file_path)
    root = tree.getroot()
    all_data = []
    for child in root:
        item = {key: child.find(key).text if child.find(key) is not None else None for key in keys}
        all_data.append(item)
    df = pd.DataFrame(all_data)
    return df

def process_files(csv_file, json_file, xml_file, keys):
    csv_df = read_csv(csv_file, keys)
    json_df = read_json(json_file, keys)
    xml_df = read_xml(xml_file, keys)
    
    combined_df = [csv_df, json_df, xml_df]
    return combined_df

def sendToKafkaProducer(topic, result_df):
    for i in result_df:
        producer.produce(topic, key='key', value='{}'.format(i), callback=delivery_report)
        producer.poll(1)


# Produce a message
# for i in range(10):
#     producer.produce(topic, key='key', value='value #{}'.format(i), callback=delivery_report)
#     # Wait up to 1 second for events. Callbacks will be invoked during
#     # this method call if the message is acknowledged.
#     producer.poll(1)

# Wait for any outstanding messages to be delivered and delivery reports
# to be received.

json_df = read_json(json_file_path, keys)

# result_df = process_files(csv_file_path, json_file_path, xml_file_path, keys)
print("result_df:", json_df)
sendToKafkaProducer(topic, json_df)
# producer.flush()