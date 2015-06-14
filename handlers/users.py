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

from model.tag import Tag
from model.game import Game
from model.user import User
from model.friend import Friend

from data import user_data

class UserTagsHandler(webapp.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        user = User.get_by_key_name(user_id)
        if user:
            tags = user_data.get_recent_tags(user_id)
            self.response.out.write(tags)

class UserLoginHandler(webapp.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        User(key_name=user_id).put()

class UserFriendsHandler(webapp.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        user = User.get_by_key_name(user_id)
        if user:
            self.response.write(user.friends)
            #friends = user_data.get_friends(user_id)
            #friends_recent_tags = user_data.get_recent_player_tags(friends)
            #template_values = {'friends_recent_tags': friends_recent_tags}
            #path = 'templates/show_friends.html'
            #self.response.out.write(template.render(path, template_values))

class GetFriendsHandler(webapp.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        user = User.get_by_key_name(user_id)
        friends_json = user_data.friends(user_id)
        for friend in friends_json['friendslist']['friends']:
            Friend.create(friend['steamid'], user)



application = webapp.WSGIApplication([  ('/user/tags', UserTagsHandler),
                                        ('/user/friends/tmp', UserFriendsHandler),
                                        ('/user/login', UserLoginHandler),
                                        ('/user/friends', GetFriendsHandler)], debug=True)
