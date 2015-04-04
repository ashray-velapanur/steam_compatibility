from google.appengine.ext import db

from model.genre import genres

class Game(db.Model):
    name = db.StringProperty(indexed=False)
    tags = db.StringListProperty(indexed=False)

    @property
    def genres(self):
        return [tag for tag in self.tags if tag in genres]
