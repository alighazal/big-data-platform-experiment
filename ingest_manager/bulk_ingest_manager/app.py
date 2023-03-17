import os,json, pika
import uuid, datetime
from models import engine, Base, ProjectConstraints
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from google.oauth2 import service_account
from google.cloud import storage




UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'parquet', 'txt'}
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bucket_name = "cassandra-pipeline-test" 
with open('./test-ghazal-0a4996a23258.json') as source:
    info = json.load(source)
storage_credentials = service_account.Credentials.from_service_account_info(info)
storage_client = storage.Client( project="test-ghazal", credentials=storage_credentials)
bucket = storage_client.bucket(bucket_name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_bulk_ingest_event(queue_name, bucket_name, blob_name ):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    ignest_event  = {"bucket_name": bucket_name, "blob_name": blob_name }
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(ignest_event) )
    print(" Sent Bucket Details'")
    connection.close()

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

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part

    project_name =  request.form["project-name"]

    if "project-name" not in request.form:
        return {"response": "project not defined"}

    if 'file' not in request.files:
        return {"response": "No file part"}
    
    file = request.files['file']

    if file.filename == '':
        return {"response": "No selected file"}

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        blob = bucket.blob(filename) 
        blob.upload_from_string(file.read())
        send_bulk_ingest_event( project_name, bucket_name=bucket_name, blob_name=blob.name )
        return {"response": "upload successful"}
    
    return {"response": "upload erorr"}
    # curl -F 'file=@./command.txt' localhost:5500/upload


app.run(host='localhost', port=5500)

