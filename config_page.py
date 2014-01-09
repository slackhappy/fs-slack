import config
import context
import webapp2
from google.appengine.api import users

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
    template = context.jinja_environment.get_template('config.html')
    self.response.out.write(template.render(template_values))
