from google.appengine.ext import db
from google.appengine.api import urlfetch

import json
import logging
import urllib

from config import STEAM_KEY

class User(db.Model):
    name = db.StringProperty(indexed=False)
    genre_scores = db.StringProperty(indexed=False)
    games = db.StringListProperty(indexed=False)
    avatar = db.StringProperty(indexed=False)

    @property
    def id(self):
        return self.key().name()
