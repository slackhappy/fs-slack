from google.appengine.ext import db

CONFIG = None

class Config(db.Model):
  api_token = db.StringProperty()
  incoming_webhook_token = db.StringProperty()
  team_domain = db.StringProperty()

def get_config():
  global CONFIG
  if not CONFIG:
    CONFIG = Config.get_by_key_name('singleton')
  else:
    CONFIG
  return CONFIG

def set_config(incoming_webhook_token, team_domain, api_token):
  Config(
    key_name='singleton',
    incoming_webhook_token=incoming_webhook_token,
    api_token=api_token,
    team_domain=team_domain).put()
  CONFIG = Config.get_by_key_name('singleton')


def has_config():
  return get_config() != None
