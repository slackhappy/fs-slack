import config
import json
import urllib2
import urllib
import logging

class Attachment(object):
  def __init__(self, value, fallback=None, text=None, pretext=None, color=None, title=None, short=None):
    self.value = value
    self.fallback=fallback
    self.text=text
    self.pretext=pretext
    self.color=color
    self.title=title
    self.short = True if short else False

  def render(self):
    attachment = {
      'fallback': self.fallback,
      'text': self.text,
      'pretext': self.pretext,
      'color': self.color,
      'fields': [{
        'title': self.title,
        'value': self.value,
        'short': self.short,
      }]
    }

    for obj in [attachment['fields'][0], attachment]:
      for key in obj.keys():
        if not obj[key]:
          del obj[key]

    return attachment

class BaseSlack:
  def post(self, text, channel=None, username=None, icon_emoji=None, attachments=None):
    pass

  def render_webhook_payload(self, text, channel=None, username=None, icon_emoji=None, attachments=None):
    if attachments is None:
      attachments = []

    payload = {
      'text': text,
      'channel': channel,
      'username': username,
      'icon_emoji': icon_emoji,
      'attachments': map(lambda attachment: attachment.render(), attachments),
    }

    for key in payload.keys():
      if not payload[key]:
        del payload[key]

    return payload

class TestSlack(BaseSlack):
  def __init__(self):
    self.last_payload = None
  def post(self, text, channel=None, username=None, icon_emoji=None, attachments=None):
     self.last_payload = self.render_webhook_payload(text, channel, username, icon_emoji, attachments)

class Slack(BaseSlack):
  def post(self, text, channel=None, username=None, icon_emoji=None, attachments=None):
    payload = self.render_webhook_payload(text, channel, username, icon_emoji, attachments)

    logging.info(payload)

    encoded_data = urllib.urlencode({'payload': json.dumps(payload)})
    logging.info(encoded_data)
    cfg = config.get_config()
    res = urllib2.urlopen(
        'https://{0}.slack.com/services/hooks/incoming-webhook?token={1}'.format(
            cfg.team_domain,
            cfg.incoming_webhook_token),
        encoded_data,
        2.0)
    logging.info(res.getcode())
    return res
