import json
import os
from datetime import datetime, date

from depot.io.interfaces import FileStorage
from depot.manager import DepotManager
from depot.fields.sqlalchemy import UploadedFileField
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'

db = SQLAlchemy(app)
"""Dokumentation & Testanfragen zu finden unter /apidocs/"""
swagger = Swagger(app)

# Depot for actual files
DepotManager.configure('default', {
    'depot.storage_path': './files'
})


class FileEncoder(json.JSONEncoder):
    def default(self, file_info):
        if isinstance(file_info, File1):
            return {
                "name": file_info.name,
                "size": file_info.size,
                "upload_date": file_info.upload_date,
                "id": file_info.id,
                "user": file_info.user,
            }
        elif isinstance(file_info, (datetime, date)):
            return file_info.isoformat()
        elif isinstance(file_info, FileStorage):
            return "str(file_info)"
        else:
            return super().default(file_info)


class File1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    size = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.Column(db.String(128))
    fileid = db.Column(UploadedFileField)

    def __init__(self, name, size, user, fileid):
        self.name = name
        self.size = size
        self.upload_date = datetime.utcnow()
        self.user = user
        self.fileid = fileid


# Create the database tables.
db.create_all()


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route("/files", methods=["GET"])
def get_files():
    """
    Get all files.
    ---
    parameters:
      - name: username
        in: query
        description: authentication token of user
        required: true
        type: string
      - name: usertoken
        in: query
        description: authentication token of user
        required: true
        type: string
    responses:
        200:
          schema:
            type: array
            items:
              type: object
              properties:
                name:
                  type: string
                size:
                  type: integer
                upload_date:
                  type: string
                id:
                  type: integer
                user:
                  type: string

    """
    # get username
    username = request.args.get("username")
    usertoken = request.args.get("usertoken")
    if not username:
        return not_authenticated(msg="Parameter 'username' is missing.")
    elif not usertoken:
        return not_authenticated(msg="Parameter 'usertoken' is missing.")
    # authenticate with token
    elif not authenticate(usertoken):
        return not_authenticated(msg="No valid token.")
    # get files from db
    db_response = File1.query.all()  # .get(user=username)
    js = json.dumps(db_response, cls=FileEncoder)
    return Response(js, status=200, mimetype='application/json')


@app.route("/files", methods=["POST"])
def add_file():
    """
    Add a new file
    ---
    operationId: add_file
    tags:
      - files
    consumes:
      - multipart/form-data
    parameters:
      - name: username
        in: formData
        description: user name
        required: true
        type: string
      - name: file_content
        in: formData
        type: file
        description: File to create
        required: true
    responses:
      202:
        description: Successfully created file
        schema:
          properties:
            name:
              type: string
            size:
              type: integer
            upload_date:
              type: string
            id:
              type: integer
            user:
              type: string
     """
    file = request.files["file_content"]
    username = request.form.get("username")
    if file:
        # depot = DepotManager.get()
        # fileid = depot.create(file)
        # stored_file = depot.get(fileid)
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file_object = File1(file.filename, file_length, "user", file)
        db.session.add(file_object)
        db.session.commit()
        js = json.dumps(file_object, cls=FileEncoder)
        return Response(js, status=201, mimetype='application/json')


@app.route("/files/<id>", methods=["DELETE"])
def delete_file(id):
    """
    Delete a File by its id
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: True
    responses:
      200:
        description: Successfully deleted a file from db
      404:
        description: Not Found
    """
    file = File1.query.get(id)
    if file:
        depot = DepotManager.get()
        depot.delete(file.fileid)
        db.session.delete(file)
        db.session.commit()
        message = {
            "message": "File removed",
        }
        return Response(json.dumps(message), status=200, mimetype='application/json')
    else:
        return not_found()
    # todo else: error


@app.route("/files/<id>", methods=["GET"])
def get_single_file(id):
    """
    Get one specific file by its id.
    ---
    parameters:
      - name: id
        in: path
        description: Id of the file
        type: integer
        required: True
    responses:
      200:
        description: Successfully found and delievered file
        schema:
          properties:
            name:
              type: string
            size:
              type: integer
            upload_date:
              type: "string"
              format: "date-time"
            id:
              type: integer
            user:
              type: string
      404:
          description: Not Found
    """
    file = File1.query.get(id)
    if file:
        js = json.dumps(file, cls=FileEncoder)
        return Response(js, status=200, mimetype='application/json')
    else:
        return not_found()


@app.route("/files/<id>/download", methods=["GET"])
def get_download_link(id):
    # StoredFile.public_url
    message = {
        "status": 404,
        "message": "Not yet implemented",
    }
    return Response(json.dumps(message), status=404)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "message": "Not Found: " + request.url,
    }
    return Response(json.dumps(message), status=404)


@app.errorhandler(401)
def not_authenticated(error=None, msg="Failed authentication!"):
    message = {
        "status": 401,
        "message": "Unauthorized: " + msg,
    }
    return Response(json.dumps(message), status=401)


def authenticate(usertoken):
    # todo add functionality
    return True


# TODO add test data
# db.session.add(File1("filename", 100, "user"))
# db.session.commit()
# db.session.add(File1("filename2", 1000, "user"))
# db.session.commit()

# start the flask loop
# app.run()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
