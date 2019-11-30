import json
import os
from datetime import datetime, date

from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from werkzeug.utils import secure_filename
from depot.io.interfaces import FileStorage
from depot.manager import DepotManager
from depot.fields.sqlalchemy import UploadedFileField
from flask import Flask, request, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_IDENTITY_CLAIM'] = 'id'

# security
app.config['JWT_SECRET_KEY'] = 'secret'  # Change this!
jwt = JWTManager(app)

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
    # todo list user freigeschaltet, für alle id (-1)
    # todo put für dateiname and freigaben
    # todo get für freigegebene Dateien mit query string parameter von get eigene zu unterscheiden
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    size = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.Column(db.Integer)
    fileobj = db.Column(UploadedFileField)

    def __init__(self, name, size, user, fileobj):
        self.name = name
        self.size = size
        self.upload_date = datetime.utcnow()
        self.user = user
        self.fileobj = fileobj


# Create the database tables.
db.create_all()


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route("/files", methods=["GET"])
@jwt_required
def get_files():
    """
    Get all files.
    ---
    securityDefinitions:
      Bearer:
        type: apiKey
        name: Authorization
        in: header
    security:
        - Bearer: []
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
    # get userid
    userid = get_jwt_identity()
    if not userid:
        return not_authenticated()
    # else: get files from db
    db_response = File1.query.filter_by(user=userid).all()
    js = json.dumps(db_response, cls=FileEncoder)
    return Response(js, status=200, mimetype='application/json')


def generate_secure_and_unique_filename(file):
    secure_name = secure_filename(file.filename)
    if not secure_name:
        secure_name = "file_without_name"
    if not File1.query.filter_by(name=secure_name).scalar():
        return secure_name
    i = 1
    while File1.query.filter_by(name=secure_name).scalar():
        secure_name = secure_name.split(".")[0] + str(i) + "." + secure_name.split(".")[1]
        i += 1
        if i > 1000:
            raise Exception()
    return secure_name


@app.route("/files", methods=["POST"])
@jwt_required
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
      - name: userid
        in: header
        description: user name
        required: true
        type: string
      - name: file_content
        in: formData
        type: file
        description: File to create
        required: true
    responses:
      201:
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
    userid = get_jwt_identity()
    if not userid:
        return not_authenticated()
    if file:
        # depot = DepotManager.get()
        # fileid = depot.create(file)
        # stored_file = depot.get(fileid)
        return create_file_obj(file, userid)
    else:
        return missing_file()


def create_file_obj(file, userid):
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0, os.SEEK_SET)
    secured_filename = generate_secure_and_unique_filename(file)
    file_object = File1(secured_filename, file_length, userid, file)
    db.session.add(file_object)
    db.session.commit()
    js = json.dumps(file_object, cls=FileEncoder)
    return Response(js, status=201, mimetype='application/json')


@app.route("/files/<file_id>", methods=["DELETE"])
@jwt_required
def delete_file(file_id):
    """
    Delete a File by its id
    ---
    parameters:
      - name: file_id
        in: path
        type: integer
        required: True
      - name: userid
        in: header
        description: authentication token of user
        required: true
        type: string
    responses:
      200:
        description: Successfully deleted a file from db
      404:
        description: Not Found
    """
    userid = get_jwt_identity()
    if not userid:
        return not_authenticated()
    file = File1.query.get(file_id)
    if file:
        if file.user != userid:
            return not_authorized()
        db.session.delete(file)
        db.session.commit()
        message = {
            "message": "File removed",
        }
        return Response(json.dumps(message), status=200, mimetype='application/json')
    else:
        return not_found()


@app.route("/files/<file_id>", methods=["GET"])
@jwt_required
def get_single_file(file_id):
    """
    Get one specific file by its id.
    ---
    parameters:
      - name: id
        in: path
        description: Id of the file
        type: integer
        required: True
      - name: usertoken
        in: header
        description: authentication token of user
        required: true
        type: string
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
    userid = get_jwt_identity()
    if not userid:
        return not_authenticated()
    file = File1.query.get(file_id)
    if file:
        if file.user != userid:
            return not_authorized()
        js = json.dumps(file, cls=FileEncoder)
        return Response(js, status=200, mimetype='application/json')
    else:
        return not_found()


@app.route("/files/<file_id>/download", methods=["GET"])
@jwt_required
def get_download(file_id):
    """
    Get the content of one specific file by its id.
    ---
    parameters:
      - name: id
        in: path
        description: Id of the file
        type: integer
        required: True
      - name: usertoken
        in: header
        description: authentication token of user
        required: true
        type: string
    responses:
      404:
        description: Not Found
    """
    userid = get_jwt_identity()
    if not userid:
        return not_authenticated()
    file = File1.query.get(file_id)
    if file:
        if file.user != userid:
            return not_authorized()
    depot = DepotManager.get()
    depot.get(file.fileobj)
    return send_file(file.fileobj.file, as_attachment=True, attachment_filename=file.fileobj.filename)


@app.route("/files/<file_id>", methods=["PATCH"])
@jwt_required
def change_filename(file_id):
    """
    Replace the name of an existing file.
    ---
    operationId: change_filename
    tags:
      - files
    consumes:
      - schema:
          type: object
            properties:
              name:
                type: string
    parameters:
      - name: userid
        in: header
        description: user id
        required: true
        type: int
      - name: file_id
        in: path
        type: integer
        required: True
      - name: file_info
        in: body
        schema:
          type: object
            properties:
              name:
                type: string
        required: True
    responses:
      200:
        description: Successfully changed file
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
      400:
        description: Missing file object
      403:
        description: Unauthorized
    """
    userid = get_jwt_identity()
    if not userid:
        return not_authenticated()
    existing_file = File1.query.get(file_id)
    if not existing_file:
        return missing_file()
    elif existing_file and existing_file.user != userid:
        return not_authorized()
    else:
        file_info = request.json
        existing_file.name = secure_filename(file_info["name"])
        existing_fileobj = existing_file.fileobj
        depot = DepotManager.get()
        depot.replace(existing_fileobj, existing_fileobj.file, filename=secure_filename(file_info["name"]))
        db.session.commit()
        file_object = File1.query.get(file_id)
        js = json.dumps(file_object, cls=FileEncoder)
        return Response(js, status=200, mimetype='application/json')


@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "message": "Not Found: " + request.url,
    }
    return Response(json.dumps(message), status=404, mimetype='application/json')


@app.errorhandler(401)
def not_authenticated(error=None, msg="Failed authentication!"):
    message = {
        "status": 401,
        "message": "Unauthorized: " + msg,
    }
    return Response(json.dumps(message), status=401, mimetype='application/json')


@app.errorhandler(403)
def not_authorized(error=None):
    message = {
        "status": 403,
        "message": "Forbidden: Insufficient access rights",
    }
    return Response(json.dumps(message), status=403, mimetype='application/json')


@app.errorhandler(400)
def missing_file(error=None):
    message = {
        "status": 400,
        "message": "Missing file",
    }
    return Response(json.dumps(message), status=400, mimetype='application/json')


# add test data
# db.session.add(File1("filename", 100, "user"))
# db.session.commit()
# db.session.add(File1("filename2", 1000, "user"))
# db.session.commit()

# start the flask loop
# app.run()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
