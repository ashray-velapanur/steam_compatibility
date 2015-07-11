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
    steamid = profile['steamid']
    name = profile['personaname']
    avatar = profile['avatar']
    recently_played_games = user_data.recently_played_games(steamid)
    genres = []
    for id in recently_played_games:
        genres.extend(game_factory.get_or_create(id).genres)
    friend_genre_scores = score.genre_scores(genres)
    user_genre_scores = json.loads(user.genre_scores)
    compatibility_score = score.compatibility(user_genre_scores, friend_genre_scores)
    friend_user = User.get_or_insert(key_name=steamid, games=recently_played_games, name=name, avatar=avatar, genre_scores=json.dumps(friend_genre_scores))
    Friend(key_name=steamid, parent=user, user=friend_user, compatibility_score=compatibility_score).put()
