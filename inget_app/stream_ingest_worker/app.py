import pika, sys, os, json
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import BatchQuery
from dateutil import parser

from data_model.journy import Journy

def main():
    rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = rmq_connection.channel()
    channel.queue_declare(queue='stream-ingest-queue')

    connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)
    create_keyspace_simple("cqlengine", replication_factor=1)
    sync_table(Journy)

    def callback(ch, method, properties, body):
        try:
            body_josn =  json.loads(body)
            print (body_josn)
            Journy.create(
                VendorID=body_josn["VendorID"],
                tpep_pickup_datetime=parser.parse (body_josn["tpep_pickup_datetime"]),
                tpep_dropoff_datetime=parser.parse (body_josn["tpep_dropoff_datetime"]),
                passenger_count=body_josn["passenger_count"],
                trip_distance=body_josn["trip_distance"],
                RatecodeID=body_josn["RatecodeID"],
                store_and_fwd_flag=body_josn["store_and_fwd_flag"],
                PULocationID=body_josn["PULocationID"],
                DOLocationID=body_josn["DOLocationID"],
                payment_type=body_josn["payment_type"],
                fare_amount=body_josn["fare_amount"],
                extra=body_josn["extra"],
                mta_tax=body_josn["mta_tax"],
                tip_amount=body_josn["tip_amount"],
                tolls_amount=body_josn["tolls_amount"],
                improvement_surcharge=body_josn["improvement_surcharge"],
                total_amount=body_josn["total_amount"],
                congestion_surcharge=body_josn["congestion_surcharge"],
                airport_fee=body_josn["airport_fee"]
                )
        except Exception as e:
            print (e)

    channel.basic_consume(queue='stream-ingest-queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)