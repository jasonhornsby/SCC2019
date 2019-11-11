from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless

# Create the Flask application and the Flask-SQLAlchemy object.

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    size = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # content = db.Column(db.)
    user = db.Column(db.String(128))


@app.route('/')
def hello_world():
    return 'Hello World!'


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/file by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(File, methods=['GET', 'POST', 'DELETE'])

# start the flask loop
app.run()

if __name__ == '__main__':
    app.run()
