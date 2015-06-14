from google.appengine.ext import db

import logging
from data import user_data

class Friend(db.Model):
    user = db.ReferenceProperty(indexed=False)
    games = db.StringListProperty(indexed=False)
