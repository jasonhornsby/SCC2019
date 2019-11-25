import json
from datetime import datetime, date

from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
CORS(app)

db = SQLAlchemy(app)
"""Dokumentation & Testanfragen zu finden unter /apidocs/"""
swagger = Swagger(app)


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
        else:
            return super().default(file_info)


class File1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    size = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # content = db.Column(db.)
    user = db.Column(db.String(128))

    def __init__(self, name, size, user):
        self.name = name
        self.size = size
        self.upload_date = datetime.utcnow()
        self.user = user


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
    # get files from db
    db_response = File1.query.all()
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
    parameters:
      - name: file_info
        in: body
        description: File to create
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            size:
              type: integer
            user:
              type: string
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
    if isinstance(request.json, str):
        file_info = json.loads(request.json)
    else:
        file_info = request.json
    file = File1(file_info["name"], file_info["size"], file_info["user"])  # TODO , default=decode_file_info
    db.session.add(file)
    db.session.commit()
    js = json.dumps(file, cls=FileEncoder)
    return Response(js, status=202, mimetype='application/json')


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


@app.errorhandler(404)
def not_found(error=None):
    message = {
        "status": 404,
        "message": "Not Found: " + request.url,
    }
    return Response(json.dumps(message), status=404)


# TODO add test data
# db.session.add(File1("filename", 100, "user"))
# db.session.commit()
# db.session.add(File1("filename2", 1000, "user"))
# db.session.commit()

# start the flask loop
# app.run()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
