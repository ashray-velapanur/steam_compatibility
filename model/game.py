from google.appengine.ext import db

class Game(db.Model):
    name = db.StringProperty(indexed=False)
    tags = db.StringListProperty(indexed=False)
