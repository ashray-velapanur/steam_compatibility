from google.appengine.ext import db

from model.games import Games
from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import json
import logging
import urllib

from model.tags import Tags
from model.games import Games

KEY = "92856D25ABD7E4B62E28A981756A0E18"

class User(db.Model):
    name = db.StringProperty(indexed=False)
    tags = db.StringListProperty(indexed=False)
    