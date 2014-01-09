import webapp2

from google.appengine.api import users

import jinja2
import os
from contextlib import contextmanager
import urllib
import json
import logging

import config
import entity
import incoming_webhook

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

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
      incoming_webhook_token = self.request.get('incoming_webhook_token')
      team_domain = self.request.get('team_domain')
      config.set_config(incoming_webhook_token, team_domain)
      self.render()

  def render(self):
    if config.has_config():
      conf = config.get_config()
      incoming_webhook_token = conf.incoming_webhook_token
      team_domain = conf.team_domain
    else:
      incoming_webhook_token = ''
      team_domain = ''

    template_values = {
      'incoming_webhook_token': incoming_webhook_token,
      'team_domain': team_domain,
    }
    template = jinja_environment.get_template('config.html')
    self.response.out.write(template.render(template_values))

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hello, World!')

class LogoutPage(webapp2.RequestHandler):
  def get(self):
    self.redirect(users.create_logout_url('/'))

class CommandPage(webapp2.RequestHandler):
  def post(self):
    logging.info(self.request)
    logging.info(self.request.get('text'))
    logging.info(self.request.get('command'))
    if self.request.get('command') == '/++':
      entity_name = self.request.get('text')
      r = entity.inc_entity(entity_name)
      incoming_webhook.incoming_webhook(entity_name + ' now at ' + str(r.score), icon_emoji=':thumbsup:')


application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/logout', LogoutPage),
  ('/config', ConfigPage),
  ('/slash', CommandPage),
], debug=True)
