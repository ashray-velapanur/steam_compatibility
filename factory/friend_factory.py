from model.friend import Friend
from model.user import User

from data import user_data
from factory import game_factory

def create(user_id, user):
    recently_played_games = user_data.recently_played_games(user_id)
    games_ids = []
    if 'total_count' in recently_played_games['response'] and recently_played_games['response']['total_count'] !=0:
        for game in recently_played_games['response']['games']:
            game_id = game['appid']
            name = game['name'] if 'name' in game else '???'
            game_factory.create(game_id, name)
            games_ids.append(str(game_id))
    friend_user = User.get_or_insert(key_name=user_id, games=games_ids)
    Friend(key_name=user_id, parent=user, user=friend_user).put()
