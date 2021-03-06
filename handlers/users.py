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

from data import user_data, score

from factory import friend_factory, game_factory

from google.appengine.ext import deferred

class UserTagsHandler(webapp.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        user = User.get_by_key_name(user_id)
        if user:
            tags = user_data.recent_tags(user_id)
            self.response.out.write(tags)

class UserLoginHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = 'templates/login.html'
        self.response.out.write(template.render(path, template_values))

    def post(self):
        user_id = self.request.get('user_id')
        recently_played_games = user_data.recently_played_games(user_id)
        profile = user_data.profiles([user_id])[0]
        avatar = profile['avatar']
        name = profile['personaname']
        genres = []
        for id in recently_played_games:
            genres.extend(game_factory.get_or_create(id).genres)
        genre_scores = score.genre_scores(genres)
        user = User.get_or_insert(key_name=user_id, games=recently_played_games, name=name, avatar=avatar, genre_scores=json.dumps(genre_scores))
        friends = user_data.friends(user_id)
        deferred.defer(friend_factory.batch_create, friends, user)

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

class UserUpdateHandler(webapp.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        user = User.get_by_key_name(user_id)
        friends = user_data.friends(user_id)
        deferred.defer(friend_factory.batch_create, friends, user)

class UserGetHandler(webapp.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        user = User.get_by_key_name(user_id)
        template_values = {}
        template_values['friends'] = []
        for friend in Friend.all().ancestor(user).order("-compatibility_score"):
            template_values['friends'].append({'genre_scores': friend.user.genre_scores, 'id': friend.user.key().name(), 'name': friend.user.name, 'avatar': friend.user.avatar, 'compatibility_score': friend.compatibility_score})
        path = 'templates/show_friends.html'
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([  ('/user/tags', UserTagsHandler),
                                        ('/user/friends/tmp', UserFriendsHandler),
                                        ('/user/login', UserLoginHandler),
                                        ('/user/update', UserUpdateHandler),
                                        ('/user/get', UserGetHandler)], debug=True)
