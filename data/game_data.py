from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import json
import logging
import urllib
import model

from bs4 import BeautifulSoup as bs

KEY = "92856D25ABD7E4B62E28A981756A0E18"

def get_tags(app_id):
    url = "http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key=%s&appid=%s"%(KEY, app_id)
    response = json.loads(urlfetch.fetch(url, deadline=60).content)
    name = response['game']['gameName']

    url_tags = 'http://store.steampowered.com/app/%s'%(app_id)
    response_tags = urlfetch.fetch(url, deadline=60).content

    tags = []
    glance_tags = bs(response_tags).find("div", {"class": "glance_tags"})
    if glance_tags:
        tag_elements = glance_tags.findAll("a", {"class": "app_tag"})
        for tag_element in tag_elements:
            tag = tag_element.string.strip()
            tags.append(tag)
    model.games.Games(key_name=str(app_id), name=name, tags=tags).put()

