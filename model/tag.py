from google.appengine.ext import db

class Tag(db.Model):
	genre = db.StringProperty(indexed=False)
