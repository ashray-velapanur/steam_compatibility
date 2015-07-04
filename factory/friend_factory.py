from model.friend import Friend
from model.user import User

from data import user_data, score
from factory import game_factory

from google.appengine.ext import deferred

import json

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
    genres = []
    for id in recently_played_games:
        genres.extend(game_factory.get_or_create(id).genres)
    genre_scores = score.genre_scores(genres)
    friend_user = User.get_or_insert(key_name=id, games=recently_played_games, name=name, avatar=avatar, genre_scores=json.dumps(genre_scores))
    Friend(key_name=id, parent=user, user=friend_user).put()
