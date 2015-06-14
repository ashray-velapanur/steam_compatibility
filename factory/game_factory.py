import logging

from google.appengine.ext import deferred

from model.game import Game

from data import game_data

def create(game_id, name):
    game = Game.get_by_key_name(str(game_id))
    logging.info('-'*80)
    logging.info(game_id)
    if game:
        logging.info('... in db')
    else:
        logging.info('... updating')
        deferred.defer(game_data.get_tags, game_id, name, _queue="fetch-data")
