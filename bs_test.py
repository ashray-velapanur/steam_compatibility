from bs4 import BeautifulSoup as bs
import urllib

app_id = '300550'
html = urllib.urlopen('http://store.steampowered.com/app/%s'%(app_id)).read()

soup = bs(html)
tags = [tag_element.string.strip() for tag_element in soup.find("div", {"class": "glance_tags"}).findAll("a", {"class": "app_tag"})]

print tags

