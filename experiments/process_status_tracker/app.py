from models import engine, Base, Process
from flask import Flask, request
from sqlalchemy.orm import Session
from sqlalchemy import select, update

import uuid, datetime
 
app = Flask(__name__)

@app.before_first_request
def create_table():
    Base.metadata.create_all(engine)

@app.route('/process/' , methods = ['POST'])
def create_a_new_process():
    process_id = str(uuid.uuid4())
    status = request.json['status']
    time = datetime.datetime.now()
    process = Process(process_id=process_id, status=status, timestamp=time)
    
    with Session(engine) as session:
        session.add(process)
        session.commit()
    return {"response": "Proccess Created"}
    # curl -d '{ "status":"value2"}' -H "Content-Type: application/json"  -X POST localhost:5000/process/


@app.route('/process/<id>' , methods = ['GET', 'PUT'])
def get_process_details(id):
    if request.method == "GET":
        stmt =  select(Process).where(Process.process_id == id )
        result = Session(engine).scalars(stmt).one()
        print(result.__dict__)
        return {"process_id": result.process_id, "status": result.status}
        # curl -X GET localhost:5000/process/b8dbf5e0-3550-4f2e-b86e-031fed05f1f0
    
    elif request.method == "PUT":
        status = request.json['status']
        stmt = update(Process).where(Process.process_id == id).values(status=status)
        with engine.begin() as conn:
            result = conn.execute(
                update(Process).where(Process.process_id == id).values(status=status)
            )
            print(result.rowcount)
        return {"response": "Proccess Updated"}
        # curl -d '{ "status":"i changed"}' -H "Content-Type: application/json"  -X PUT localhost:5000/process/b8dbf5e0-3550-4f2e-b86e-031fed05f1f0

app.run(host='localhost', port=5000)

