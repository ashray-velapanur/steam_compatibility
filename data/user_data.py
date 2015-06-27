from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import json
import logging
import urllib

from data import game_data

KEY = "92856D25ABD7E4B62E28A981756A0E18"

def friends(user_id):
    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend"%(KEY, user_id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    return response

def recently_played_games(user_id):
    url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=%s&steamid=%s&format=json"%(KEY, user_id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    ids = []
    if 'total_count' in response['response'] and response['response']['total_count'] !=0:
        ids = [str(game['appid']) for game in response['response']['games']]
    return ids
