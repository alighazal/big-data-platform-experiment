from models import engine, Base, ProjectConstraints
from flask import Flask, request
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from dateutil import parser

import uuid, datetime
 
app = Flask(__name__)

@app.before_first_request
def create_table():
    Base.metadata.create_all(engine)

@app.route('/project/' , methods = ['POST'])
def create_a_new_project():
    project_name = request.json['project_name']
    allowed_file_ext = request.json['allowed_file_ext']
    max_file_size = request.json['max_file_size']
    created_at = datetime.datetime.now()
    new_project_and_constrinsts = ProjectConstraints(project_name=project_name, allowed_file_ext=allowed_file_ext, max_file_size=max_file_size, created_at=created_at)
    
    with Session(engine) as session:
        session.add(new_project_and_constrinsts)
        session.commit()
    return {"response": "project_created"}
    # curl -d '{"project_name": "my-lovely-cat",  "allowed_file_ext": "parquet", "max_file_size": 1000000 }' -H "Content-Type: application/json"  -X POST localhost:5500/project/

@app.route('/project/<project_name>' , methods = ['GET', 'PUT'])
def get_process_details(project_name):
    if request.method == "GET":
        stmt =  select(ProjectConstraints).where(ProjectConstraints.project_name == project_name )
        result = Session(engine).scalars(stmt).one()
        print(result.__dict__)
        return {"project_name": result.project_name, 
                "allowed_file_ext": result.allowed_file_ext, 
                "max_file_size": result.max_file_size, 
                "created_at": result.created_at}
        # curl -X GET localhost:5500/project/my-lovely-cat

app.run(host='localhost', port=5500)

