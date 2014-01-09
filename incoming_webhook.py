import config
import json
import urllib2
import urllib
import logging

def incoming_webhook(text, channel=None, username=None, icon_emoji=None):
  payload = {
    'text': text,
    'channel': channel,
    'username': username,
    'icon_emoji': icon_emoji
  }

  for key in payload.keys():
    if not payload[key]:
      del payload[key]

  encoded_data = urllib.urlencode({'payload': json.dumps(payload)})
  logging.info(encoded_data)
  cfg = config.get_config()
  res = urllib2.urlopen(
    'https://{0}.slack.com/services/hooks/incoming-webhook?token={1}'.format(cfg.team_domain, cfg.incoming_webhook_token),
    encoded_data,
    2.0)
  logging.info(res.getcode())
