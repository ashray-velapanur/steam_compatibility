import logging
import json
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext import deferred

from model.game import Game

from data import game_data

def create(id):
    game = Game.get_by_key_name(str(id))
    if not game:
        details = game_data.details(id)
        logging.info('#'*80)
        logging.info(details)
        if details:
            Game(key_name=str(id), name=details['name'], genres=details['genres']).put()

#stop using this
def _create(games):
    for game in games:
        id = game['id']
        name = game['name']
        game = Game.get_by_key_name(str(id))
        logging.info('-'*80)
        logging.info(id)
        if game:
            logging.info('... in db')
        else:
            logging.info('... updating')
            deferred.defer(game_data.get_tags, id, name, _queue="fetch-data")
