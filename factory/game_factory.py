import logging

from google.appengine.ext import deferred

from model.game import Game

from data import game_data

def create(games):
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
