import datetime

from app import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    size = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.Column(db.String(128))

    def __repr__(self):
        return '<File {}>'.format(self.name)
