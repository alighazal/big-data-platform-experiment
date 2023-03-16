from flask import Flask, request
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import BatchQuery

from data_model.journy import Journy

app = Flask(__name__)

@app.before_first_request
def create_table():
    connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)
    create_keyspace_simple("cqlengine", replication_factor=1)
    sync_table(Journy)

@app.route('/yellow-taxi/journys' , methods = ['POST'])
def add_entry():
    print (request.json)
    try:
        Journy.create(
                VendorID=request.json["VendorID"],
                tpep_pickup_datetime=request.json["tpep_pickup_datetime"].to_pydatetime(),
                tpep_dropoff_datetime=request.json["tpep_dropoff_datetime"].to_pydatetime(),
                passenger_count=request.json["passenger_count"],
                trip_distance=request.json["trip_distance"],
                RatecodeID=request.json["RatecodeID"],
                store_and_fwd_flag=request.json["store_and_fwd_flag"],
                PULocationID=request.json["PULocationID"],
                DOLocationID=request.json["DOLocationID"],
                payment_type=request.json["payment_type"],
                fare_amount=request.json["fare_amount"],
                extra=request.json["extra"],
                mta_tax=request.json["mta_tax"],
                tip_amount=request.json["tip_amount"],
                tolls_amount=request.json["tolls_amount"],
                improvement_surcharge=request.json["improvement_surcharge"],
                total_amount=request.json["total_amount"],
                congestion_surcharge=request.json["congestion_surcharge"],
                airport_fee=request.json["airport_fee"]
            )
    except:
        return {"message": "error :/"}
    
    return {"message": "success :D"}

    # curl -d '{ "status":"value2"}' -H "Content-Type: application/json"  -X POST localhost:5100/process/


app.run(host='localhost', port=5100)


# curl -d '{"VendorID": "1", "tpep_pickup_datetime": "2018-01-22 18:45:57", "tpep_dropoff_datetime": "2018-01-22 18:45:57", "passenger_count": "1", "trip_distance": "1", "RatecodeID": "1", "store_and_fwd_flag": "1", "PULocationID": "1", "DOLocationID": "1", "payment_type": "1", "fare_amount": "1", "extra": "1", "mta_tax": "1", "tip_amount": "1", "tolls_amount": "1", "improvement_surcharge": "1", "total_amount": "1", "congestion_surcharge": "1", "airport_fee": "1" }' -H "Content-Type: application/json"  -X POST localhost:5100/yellow-taxi/journys
