import datetime
from flask import url_for
from flasky import db

class Video(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    vid = db.StringField(max_length=255, required=True, unique=True)
    url = db.StringField(required=False)
