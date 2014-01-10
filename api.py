import config
import json
import urllib2
import urllib
import logging

def files_upload(content, filetype=None, filename=None, title=None, channels=None):
  cfg = config.get_config()
  payload = {
    'token': cfg.api_token,
    'content': content,
    'filetype': filetype,
    'filename': filename,
    'title': title,
    'channels': ','.join(channels)
  }

  for key in payload.keys():
    if not payload[key]:
      del payload[key]
  logging.info(payload)

  encoded_data = urllib.urlencode(payload)
  res = urllib2.urlopen(
    'https://slack.com/api/files.upload',
    encoded_data,
    6.0)
  logging.info(res.getcode())
