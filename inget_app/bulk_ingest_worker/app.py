import pika, sys, os, json
from google.cloud import storage

def download_blob_from_google_storage(bucket_name, blob_name):
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    download_path = f"./data/${blob_name}"
    blob.download_to_filename( download_path )
    
    return download_path

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue='bulk-ingest-queue')

    def callback(ch, method, properties, body):
        try:
            body_josn =  json.loads(body)
            if ( "bucket_name" in body_josn and "blob_name" in body_josn ):
                downloand_path = download_blob_from_google_storage( body_josn["bucket_name"], body_josn["blob_name"] )
                # ingest file
            else:
                print ("unrecognized message format")
        except Exception:
            print ("serialziation error")

    channel.basic_consume(queue='bulk-ingest-queue', on_message_callback=callback, auto_ack=True)

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