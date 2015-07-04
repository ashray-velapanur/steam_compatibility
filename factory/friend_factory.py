from model.friend import Friend
from model.user import User

from data import user_data
from factory import game_factory

from google.appengine.ext import deferred

#this could be better written
def batch_create(ids, user):
    chunks = [ids[x : x + 25] for x in xrange(0, len(ids), 25)]
    for chunk in chunks:
        profiles = user_data.profiles(chunk)
        for profile in profiles:
            deferred.defer(create, profile, user)    

def create(profile, user):
    id = profile['steamid']
    name = profile['personaname']
    avatar = profile['avatar']
    recently_played_games = user_data.recently_played_games(id)
    deferred.defer(game_factory.batch_create, recently_played_games)
    friend_user = User.get_or_insert(key_name=id, games=recently_played_games, name=name, avatar=avatar)
    Friend(key_name=id, parent=user, user=friend_user).put()
