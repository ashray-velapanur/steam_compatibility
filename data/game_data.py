from google.appengine.api import urlfetch
from google.appengine.ext import deferred

import json
import logging
import urllib

from model.games import Games

from bs4 import BeautifulSoup as bs

KEY = "92856D25ABD7E4B62E28A981756A0E18"

def update(app_id, name):
    game = Games.get_by_key_name(str(app_id))
    logging.info('-'*80)
    logging.info(app_id)
    if game:
        logging.info('... in db')
        return game
    else:
        logging.info('... updating')
        deferred.defer(get_tags, app_id, name, _queue="fetch-data")


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
    Games(key_name=str(app_id), name=name, tags=tags).put()

