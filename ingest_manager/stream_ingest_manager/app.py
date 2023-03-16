from flask import Flask, request
import pika
import json

app = Flask(__name__)

@app.route('/yellow-taxi/journys' , methods = ['POST'])
def send_event_to_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue='stream-ingest-queue')
    channel.basic_publish(exchange='', routing_key='stream-ingest-queue', body= json.dumps(request.json) )
    connection.close()
    return {"message": "event emitted"}


app.run(host='localhost', port=5100)


# curl -d '{"VendorID": 1, "tpep_pickup_datetime": "2022-01-01 00:35:40", "tpep_dropoff_datetime": "2022-01-01 00:53:29", "passenger_count": 2.0, "trip_distance": 3.8, "RatecodeID": 1.0, "store_and_fwd_flag": "N", "PULocationID": 142, "DOLocationID": 236, "payment_type": 1, "fare_amount": 14.5, "extra": 3.0, "mta_tax": 0.5, "tip_amount": 3.65, "tolls_amount": 0.0, "improvement_surcharge": 0.3, "total_amount": 21.95, "congestion_surcharge": 2.5, "airport_fee": 0.0 }' -H "Content-Type: application/json"  -X POST localhost:5100/yellow-taxi/journys
# curl -d '{"VendorID": "1", "tpep_pickup_datetime": "01-01-1999", "tpep_dropoff_datetime": "01-01-1999", "passenger_count": "1", "trip_distance": "1", "RatecodeID": "1", "store_and_fwd_flag": "1", "PULocationID": "1", "DOLocationID": "1", "payment_type": "1", "fare_amount": "1", "extra": "1", "mta_tax": "1", "tip_amount": "1", "tolls_amount": "1", "improvement_surcharge": "1", "total_amount": "1", "congestion_surcharge": "1", "airport_fee": "1" }' -H "Content-Type: application/json"  -X POST localhost:5100/yellow-taxi/journys