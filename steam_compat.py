import json
import urllib
from bs4 import BeautifulSoup as bs

KEY = "92856D25ABD7E4B62E28A981756A0E18"

FRIENDS_URL = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=%s&steamid=%s&relationship=friend"%(KEY, '76561198000951390')

PROFILE_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s"%(KEY, '%s')

#friends = json.loads(urllib.urlopen(FRIENDS_URL).read())

#for friend in friends['friendslist']['friends']:
#	profile = json.loads(urllib.urlopen(PROFILE_URL%friend['steamid']).read())
#	print profile
#	break

def get_recently_played_games(user_id):
	url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=%s&steamid=%s&format=json"%(KEY, user_id)
	response = json.loads(urllib.urlopen(url).read())
	return response['response']['games']

def get_tags(app_id):
	url = 'http://store.steampowered.com/app/%s'%(app_id)
	response = urllib.urlopen(url).read()
	tags = [tag_element.string.strip().lower() for tag_element in bs(response).find("div", {"class": "glance_tags"}).findAll("a", {"class": "app_tag"})]
	return tags

games = get_recently_played_games('76561198000951390')
app_ids = [game['appid'] for game in games]
print get_tags(app_ids[1])