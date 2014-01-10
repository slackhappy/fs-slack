import config
import context
import webapp2
import logging
from google.appengine.api import users

CONFIG_KEYS = ['team_domain', 'incoming_webhook_token', 'api_token']

class ConfigPage(webapp2.RequestHandler):

  def ensure_admin(self):
    user = users.get_current_user()
    if user:
      if users.is_current_user_admin():
        return True
      else:
        self.error(500)
        return False
    else:
      self.redirect(users.create_login_url(self.request.uri))

  def get(self):
    if self.ensure_admin():
      self.render()

  def post(self):
    if self.ensure_admin():
      settings = {}
      for key in CONFIG_KEYS:
        settings[key] = self.request.get(key)
        if not settings[key]:
          settings[key] = ''
      logging.info(settings)
      config.set_config(**settings)
      self.render()

  def render(self):
    conf = config.get_config()
    settings = {}
    for key in CONFIG_KEYS:
      if hasattr(conf, key):
        settings[key] = getattr(conf, key)
      else:
        settings[key] = ''
    template = context.jinja_environment.get_template('config.html')
    self.response.out.write(template.render(settings))
