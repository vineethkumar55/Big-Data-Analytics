**Title** 
Design of Real time Distributed Heterogenous System to deal with Stream loss 

**Overview**
This project implements a distributed heterogeneous stream-disk join architecture designed to address challenges such as stream loss, scalability, disk access, and data accuracy in real-time processing applications. The architecture is composed of several key components:

- **Pre-processing Module**: Converts heterogeneous streams into homogeneous streams.
- **Real-time Disk Access Module**: Retrieves and integrates distributed disk data with processed stream data.
- **Stream-Disk Join Module**: Combines pre-processed stream data and distributed disk data using a distributed in-memory database.
- **Data Visualization Tool**: Provides real-time visualization of streaming data.
- **Logging and Analysis Module**: Captures and exports logs for further analysis.

This approach ensures robust and efficient real-time data processing.

## Features

- Efficiently collects and stores diverse stream messages using Apache Kafka.
- Pre-processes heterogeneous streams into a homogeneous format with Apache Spark.
- Performs real-time disk access and join operations with Apache Spark and MongoDB.
- Integrates with the ELK Stack for real-time data visualization and monitoring.
- Captures and exports logs for performance analysis and optimization.

## Installation

### Prerequisites

- Apache Kafka
- Apache Spark
- MongoDB
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Python 3.x
- Confluent Kafka Python client

