from model.friend import Friend
from model.user import User

from data import user_data
from factory import game_factory

def create(user_id, user):
    recently_played_games = user_data.recently_played_games(user_id)
    ids = []
    for game in recently_played_games:
        ids.append(str(game['id']))
        game_factory.create(game['id'], game['name'])
    friend_user = User.get_or_insert(key_name=user_id, games=ids)
    Friend(key_name=user_id, parent=user, user=friend_user).put()
