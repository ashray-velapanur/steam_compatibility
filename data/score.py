from model.user import User
from model.game import Game
from model.genre import mapping

def for_user(user_id):
	user = User.get_by_key_name(user_id)
	scores = {}
	for id in user.games:
		tags = Game.get_by_key_name(id).tags
		for tag in tags:
			tag = tag.lower()
			if tag in mapping:
				for genre in mapping[tag]:
					if not genre in scores:
						scores[genre] = 0
					scores[genre] +=1
	return scores

def compatibility(user_id_1, user_id_2):
	user_1_tags = for_user(user_id_1)
	user_2_tags = for_user(user_id_2)
	return len(user_2_tags.viewkeys() & user_1_tags.viewkeys())