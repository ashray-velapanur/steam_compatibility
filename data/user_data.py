from model.games import Games
from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import json
import logging
import urllib

from model.tags import Tags
from model.games import Games

KEY = "92856D25ABD7E4B62E28A981756A0E18"


def get_recently_played_games(user_id):
    url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=%s&steamid=%s&format=json"%(KEY, user_id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    return response['response']['games']

def get_recent_tags(user_id):
    recently_played = get_recently_played_games(user_id)
    tags = []
    for game in recently_played:
        app_id = str(game['appid'])
        game_object = Games.get_or_update(app_id)
        if game_object:
            tags.extend(game_object.tags)
    return tags

def get_friends(user_id):
    friends = {}
    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend"%(KEY, user_id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    ids = [friend['steamid'] for friend in response['friendslist']['friends']] 
    ids = ids[0:10] ### remove this limit
    ids = ",".join(ids)
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s"%(KEY, ids)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    return response['response']['players']


def get_profiles(ids):
    ids = ids[0:10] ### remove this limit
    ids = ",".join(ids)
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s"%(KEY, ids)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    return response['response']['players']

def get_friends_ids(user_id):
    friends = {}
    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend"%(KEY, user_id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    friend_ids = [friend['steamid'] for friend in response['friendslist']['friends']] 
    return friend_ids
