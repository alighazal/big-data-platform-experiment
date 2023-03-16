import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='bulk-ingest-queue')

channel.basic_publish(exchange='', routing_key='bulk-ingest-queue', body='{ "bucket_name": "cassandra-pipeline-test", "blob_name": "yellow_tripdata_2022-01.parquet" }')
print(" Sent Bucket Details'")
connection.close()