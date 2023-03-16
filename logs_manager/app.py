from models import engine, Base, IngestionEvent
from flask import Flask, request
from sqlalchemy.orm import Session
from sqlalchemy import select, update

import uuid, datetime
 
app = Flask(__name__)

@app.before_first_request
def create_table():
    Base.metadata.create_all(engine)

@app.route('/log/' , methods = ['POST'])
def create_a_new_log_entery():
    id = str(uuid.uuid4())
    src = request.json['src']
    status = request.json['status']
    records_count = request.json['records_count']
    timestamp = datetime.datetime.now()
    ingest_event = IngestionEvent(id=id, src=src, records_count = records_count, status=status, timestamp=timestamp)
    
    with Session(engine) as session:
        session.add(ingest_event)
        session.commit()
    return {"response": "event logged"}
    # curl -d '{ "src":"messaging", "records_count" : 30, "status": "success" }' -H "Content-Type: application/json"  -X POST localhost:5300/log/


app.run(host='localhost', port=5300)

