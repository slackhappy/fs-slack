from google.appengine.ext import db

class Entity(db.Model):
  score = db.IntegerProperty()

def inc_entity(name, delta=1):
  entity = Entity.get_or_insert(name, score=0)
  entity.score += delta
  entity.put()
  return entity
