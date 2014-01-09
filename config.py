from google.appengine.ext import db

class Config(db.Model):
  incoming_webhook_token = db.StringProperty()
  team_domain = db.StringProperty()

def get_config():
  return Config.get_by_key_name('singleton')

def set_config(incoming_webhook_token, team_domain):
  Config(
    key_name='singleton',
    incoming_webhook_token=incoming_webhook_token,
    team_domain=team_domain).put()

def has_config():
  return get_config() != None
