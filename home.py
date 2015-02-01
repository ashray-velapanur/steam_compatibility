from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from google.appengine.ext import deferred
from google.appengine.ext.webapp import template

import json
import logging
import urllib

import os

from bs4 import BeautifulSoup as bs

from model.tags import Tags
from model.games import Games

KEY = "92856D25ABD7E4B62E28A981756A0E18"


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


class FetchData(webapp.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        recently_played = get_recently_played_games(user_id)
        for game in recently_played:
            deferred.defer(fetch_game_data, game, _queue="fetch-data")

class ShowFriends(webapp.RequestHandler):
    def post(self):
        user_id = self.request.get('user_id')
        friends_ids = get_friends_ids(user_id)
        friends = get_profiles(friends_ids)
        template_values = {'friends': friends}
        path = os.path.join(os.path.dirname(__file__), 'templates/show_friends.html')
        self.response.out.write(template.render(path, template_values))

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = None
        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([  ('/', MainPage),
                                        ('/fetch_data', FetchData),
                                        ('/show_friends', ShowFriends)],
                                        debug=True)
