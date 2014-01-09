from google.appengine.ext import db

class Entity(db.Model):
  score = db.IntegerProperty()

def inc_entity(name):
  entity = Entity.get_or_insert(name, score=0)
  entity.score += 1
  entity.put()
  return entity
