from model.friend import Friend
from model.user import User

from data import user_data
from factory import game_factory

from google.appengine.ext import deferred

def create(user_id, user):
    recently_played_games = user_data.recently_played_games(user_id)
    for id in recently_played_games:
        game_factory.create(id)
    friend_user = User.get_or_insert(key_name=user_id, games=recently_played_games)
    Friend(key_name=user_id, parent=user, user=friend_user).put()
