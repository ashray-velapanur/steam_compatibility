from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import logging

from model.tags import Tags
from data import game_data

from bs4 import BeautifulSoup as bs

KEY = "92856D25ABD7E4B62E28A981756A0E18"

class Games(db.Model):
    name = db.StringProperty(indexed=False)
    tags = db.StringListProperty(indexed=False)

    @classmethod
    def get_or_update(cls, app_id):
        game = Games.get_by_key_name(app_id)
        if game:
            return game
        else:
            deferred.defer(game_data.get_tags, app_id, _queue="fetch-data")
