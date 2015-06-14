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

def get_recent_tags(user_id):
    recently_played = get_recently_played_games(user_id)
    tags = set()
    for game in recently_played:
        app_id = str(game['appid'])
        name = game['name']
        game_object = game_data.get_or_update(app_id, name)
        if game_object:
            tags |= set(game_object.tags)
    return tags

def recently_played_games(user_id):
    url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=%s&steamid=%s&format=json"%(KEY, user_id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    return response
    #return response['response']['games'] if response['response']['total_count'] != 0 else []

''''
old code
'''

def get_weighted_recent_tags(user_id):
    recently_played = get_recently_played_games(user_id)
    weighted_tags = {}
    for game in recently_played:
        app_id = str(game['appid'])
        if 'name' in game:          ### some games don't have names?
            name = game['name']
            game_object = game_data.get_or_update(app_id, name)
            if game_object:
                logging.info('... play time')
                logging.info(game)
                for tag in game_object.genres:
                    if not tag in weighted_tags:
                        weighted_tags[tag] = 0
                    weighted_tags[tag] += 1
    return weighted_tags


def get_friends(user_id):
    friends = {}
    friends_url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend"%(KEY, user_id)
    friends_response = json.loads(urlfetch.fetch(friends_url, deadline=60).content)
    ids = [friend['steamid'] for friend in friends_response['friendslist']['friends']] 
    ids = ids[0:10] ### remove this limit
    ids = ",".join(ids)
    profiles_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s"%(KEY, ids)
    profiles_response = json.loads(urlfetch.fetch(profiles_url, deadline=60).content)
    return profiles_response['response']['players']

def get_recent_player_tags(players):
    recent_tags = []
    for player in players:
        recent_tags_dict = {}
        recent_tags_dict['name'] = player['personaname']
        recent_tags_dict['avatar'] = player['avatar']
        recent_tags_dict['recent_tags'] = get_recent_tags(player['steamid'])
        recent_tags.append(recent_tags_dict)
    return recent_tags

def get_friends_recent_tags(user_id):
    friends = get_friends(user_id)
    friends_recent_tags = []
    for friend in friends:
        friends_recent_tags_dict = {}
        friends_recent_tags_dict['name'] = friend['personaname']
        friends_recent_tags_dict['avatar'] = friend['avatar']
        friends_recent_tags_dict['recent_tags'] = get_weighted_recent_tags(friend['steamid'])
        #friends_recent_tags_dict['recent_tags'] = get_recent_tags(friend['steamid'])
        friends_recent_tags.append(friends_recent_tags_dict)
    return friends_recent_tags
