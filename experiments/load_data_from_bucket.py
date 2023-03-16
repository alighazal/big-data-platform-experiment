from google.cloud import storage

def download_blob_from_google_storage(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(blob_name)

bucket_name = "cassandra-pipeline-test"
blob_name = "yellow_tripdata_2022-01.parquet"
download_blob_from_google_storage(bucket_name, blob_name)
