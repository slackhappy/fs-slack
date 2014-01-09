import logging
import webapp2
from google.appengine.api import users

from config_page import ConfigPage
import commands
import context
import entity


class MainPage(webapp2.RequestHandler):
  def get(self):
    template = context.jinja_environment.get_template('index.html')
    self.response.out.write(template.render({}))

class LogoutPage(webapp2.RequestHandler):
  def get(self):
    self.redirect(users.create_logout_url('/'))

class CommandPage(webapp2.RequestHandler):
  def post(self):
    logging.info(self.request)
    logging.info(self.request.get('text'))
    logging.info(self.request.get('command'))
    commands.run(self.request)

application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/logout', LogoutPage),
  ('/config', ConfigPage),
  ('/slash', CommandPage),
], debug=True)
