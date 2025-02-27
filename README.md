
# Real-time User Data Pipeline with Airflow, Kafka, Spark Structured Streaming, and Cassandra

A data pipeline that streams user data from an API, processes it in real-time, and stores it in Cassandra.

## Technologies Used
- **Apache Airflow**: Data orchestration
- **Apache Kafka**: Real-time data streaming
- **Apache Spark**: Stream processing
- **Cassandra**: NoSQL database for storage
- **Docker**: Containerization

## Architecture

![Screenshot 2025-02-27 at 13 43 47](https://github.com/user-attachments/assets/74b9c1f2-23e7-4f35-ba26-a64dd183772e)



## Setup Instructions

### 1. Clone Repository
```bash
git clone [my-repo-url]
cd project-directory
```

### 2. Directory Structure

├── dags/
│   └── kafka_stream.py
│   └── streaming_to_kafka.py
├── spark_stream.py
├── docker-compose.yml
├── requirements.txt
└── script/
    └── entrypoint.sh

## How to run

### 1. Start Docker Containers
```bash
docker-compose up -d
```

### 2. Initialize Airflow
1. Access Airflow UI: `http://localhost:8080`
2. Enable `push_data_to_broker` DAG

   ![Screenshot 2025-02-27 at 01 24 33](https://github.com/user-attachments/assets/817d8145-b575-40fc-8bc0-b132951aa16e)


### 3. Check the condition of Zookeeper and Broker via control center (Confluent at port 9021).

  ![Screenshot 2025-02-27 at 12 44 29](https://github.com/user-attachments/assets/9a35f149-6faf-4800-b56d-1210116e723a)

### 4. Access the message of users_profile's Topic to see data which were being pushed from the random api by Airflow.

  ![Screenshot 2025-02-27 at 01 26 28](https://github.com/user-attachments/assets/3966e623-a7bf-4bf8-aa69-6c707ea2a5bc)
### 5. Go to the terminal to copy the spark_stream.py from the local to the spark-worker container, then access the spark-worker container.

```bash
docker cp path/to/spark_stream.py kafka-spark-worker-1:opt/bitnami/spark
``` 
![Screenshot 2025-02-27 at 01 29 27](https://github.com/user-attachments/assets/690d9b60-1f42-4191-afc5-1b9c615fb416)


```bash
docker exec -it kafka-spark-worker-1 bash
``` 
![Screenshot 2025-02-27 at 00 28 03](https://github.com/user-attachments/assets/d9952f35-5c76-4ebe-93c7-a5d55a1b1970)

### 6. Trigger the spark structured streaming by command.
```bash
spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 spark_stream.py
```

![Screenshot 2025-02-27 at 03 12 02](https://github.com/user-attachments/assets/3d71d1af-acc8-4456-87a1-71a0203cf07e)

### 7. Check the Cassandra via terminal:
```bash
docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042
```

<img width="864" alt="Screenshot 2025-02-27 at 13 06 33" src="https://github.com/user-attachments/assets/40a7c926-765f-4521-baa8-7ece5f25df04" />

## Key Components

### 1. Docker Services
| Service | Port | Description |
|---------|------|-------------|
| Airflow | 8080 | Workflow orchestration |
| Kafka | 9092 | Message brokering |
| Cassandra | 9042 | Data storage |
| Spark Master | 7077 | Cluster management |
| Control Center | 9021 | Kafka monitoring |

### 2. Airflow DAG (`dag.py`)
- Fetches data from `randomuser.me`
- Formats user profiles
- Streams to Kafka topic `users_profile`

### 3. Spark Streaming (`spark_stream.py`)
- Consumes from Kafka topic
- Creates Cassandra schema
- Writes to `spark_streams.users_profile` table

## Useful links

https://mvnrepository.com/artifact/org.apache.spark/spark-sql-kafka-0-10

https://mvnrepository.com/artifact/com.datastax.spark/spark-cassandra-connector

https://spark.apache.org/docs/3.5.1/structured-streaming-kafka-integration.html


