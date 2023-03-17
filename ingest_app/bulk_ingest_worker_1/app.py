import pika, sys, os, json
from google.cloud import storage
from google.oauth2 import service_account
import pandas as pd
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection as cassandra_connection
from cassandra.cqlengine.query import BatchQuery
from data_model.journy import Journy

def download_blob_from_google_storage(bucket_name, blob_name):
    with open('./test-ghazal-0a4996a23258.json') as source:
        info = json.load(source)
    storage_credentials = service_account.Credentials.from_service_account_info(info)
    storage_client = storage.Client( project="test-ghazal", credentials=storage_credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    download_path = os.path.join("./downloads/", f"downloaded-{blob_name}")
    print (download_path)
    blob.download_to_filename( download_path )
    
    return download_path

def bulk_ingest(data_path):
    
    df = pd.read_parquet(data_path)
    batch_size = 100
    for index in range(0, len(df), batch_size):
        with BatchQuery() as b:
            for i, row in df[index: index + batch_size].iterrows():
                Journy.batch(b).create(
                    VendorID=row["VendorID"],
                    tpep_pickup_datetime=row["tpep_pickup_datetime"].to_pydatetime(),
                    tpep_dropoff_datetime=row["tpep_dropoff_datetime"].to_pydatetime(),
                    passenger_count=row["passenger_count"],
                    trip_distance=row["trip_distance"],
                    RatecodeID=row["RatecodeID"],
                    store_and_fwd_flag=row["store_and_fwd_flag"],
                    PULocationID=row["PULocationID"],
                    DOLocationID=row["DOLocationID"],
                    payment_type=row["payment_type"],
                    fare_amount=row["fare_amount"],
                    extra=row["extra"],
                    mta_tax=row["mta_tax"],
                    tip_amount=row["tip_amount"],
                    tolls_amount=row["tolls_amount"],
                    improvement_surcharge=row["improvement_surcharge"],
                    total_amount=row["total_amount"],
                    congestion_surcharge=row["congestion_surcharge"],
                    airport_fee=row["airport_fee"]
                )


def main():
    msq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = msq_connection.channel()
    channel.queue_declare(queue='my-lovely-cat')

    cassandra_connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)
    sync_table(Journy)

    def callback(ch, method, properties, body):
        print (body)
        try:
            body_josn =  json.loads(body.decode("utf-8") )
            if ( "bucket_name" in body_josn and "blob_name" in body_josn ):
                downloand_path = download_blob_from_google_storage( body_josn["bucket_name"], body_josn["blob_name"] )
                # TODO ingest file
                bulk_ingest(downloand_path)
            else:
                print ("unrecognized message format")
        except Exception as e:
            print (e)
            print ("serialziation error")

    channel.basic_consume(queue='my-lovely-cat', on_message_callback=callback, auto_ack=True)

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