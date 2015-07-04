from model.user import User
from model.game import Game
from model.genre import mapping

import logging

def for_user(user):
	scores = {}
	for id in user.games:
		logging.info('#'*80)
		logging.info(id)
		game = Game.get_by_key_name(id)
		if not game:
			logging.info('no game')
			continue
		genres = game.genres
		for genre in genres:
			genre = genre.lower()
			if not genre in scores:
				scores[genre] = 0
			scores[genre] +=1
	return scores

def compatibility(user_1, user_2):
	user_1_tags = for_user(user_1)
	user_2_tags = for_user(user_2)
	logging.info('$'*80)
	logging.info(user_1_tags)
	logging.info(user_2_tags)
	return len(user_2_tags.viewkeys() & user_1_tags.viewkeys())