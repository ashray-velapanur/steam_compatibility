from google.appengine.ext import db

import logging
from data import user_data

class Friend(db.Model):
    user = db.ReferenceProperty(indexed=False)
    games = db.StringListProperty(indexed=False)

    @classmethod
    def create(cls, user_id, user):
    	recently_played_games = user_data.recently_played_games(user_id)
    	games_ids = []
    	if 'total_count' in recently_played_games['response'] and recently_played_games['response']['total_count'] !=0:
    		games_ids = [str(game['appid']) for game in recently_played_games['response']['games']]
		cls(key_name=user_id, parent=user, games=games_ids).put()
