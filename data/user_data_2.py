from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import json
import logging
import urllib

from config import STEAM_KEY

def friends_ids(user_id):
    url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend"%(STEAM_KEY, user_id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    ids = [friend['steamid'] for friend in response['friendslist']['friends']] 
    ids = ids[0:20]
    return ids

def profiles(user_ids):
    user_ids = ",".join(user_ids)
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s"%(STEAM_KEY, user_ids)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    return response['response']['players']
