from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import json
import logging
import urllib

from model.game import Game
from model.tag import Tag

from bs4 import BeautifulSoup as bs

def get_tags(app_id, name):
    url_tags = 'http://store.steampowered.com/app/%s'%(app_id)
    response_tags = urlfetch.fetch(url_tags, deadline=60).content

    tags = []
    glance_tags = bs(response_tags).find("div", {"class": "glance_tags"})
    if glance_tags:
        tag_elements = glance_tags.findAll("a", {"class": "app_tag"})
        for tag_element in tag_elements:
            tag = tag_element.string.strip()
            tags.append(tag)
            Tag(key_name=tag).put()
    Game(key_name=str(app_id), name=name, tags=tags).put()

def details(id):
    url = "http://store.steampowered.com/api/appdetails/?appids=%s"%(id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    if id in response and response[id]['success'] == True:
        name = response[id]['data']['name']
        genres = []
        if 'genres' in response[id]['data']:
            genres = [genre['description'] for genre in response[id]['data']['genres']]
        return {'name': name, 'genres': genres}
