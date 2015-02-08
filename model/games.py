from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import logging

from bs4 import BeautifulSoup as bs

KEY = "92856D25ABD7E4B62E28A981756A0E18"

class Games(db.Model):
    name = db.StringProperty(indexed=False)
    tags = db.StringListProperty(indexed=False)
