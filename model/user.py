from google.appengine.ext import db
from google.appengine.api import urlfetch

import json
import logging
import urllib

from config import STEAM_KEY
from data import user_data_2 as user_data

class User(db.Model):
    name = db.StringProperty(indexed=False)
    tags = db.StringListProperty(indexed=False)
    games = db.StringListProperty(indexed=False)

    @property
    def id(self):
        return self.key().name()

    @property
    def friends(self):
        friends_ids = user_data.friends_ids(self.id)
        friends_profiles = user_data.profiles(friends_ids)
        return friends_profiles