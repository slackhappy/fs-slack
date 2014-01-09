import entity
import incoming_webhook
import logging
import re

REGISTRY = {}

def register(name, fn):
  global REGISTRY
  REGISTRY[name] = fn

def run(req):
  command = Command(req)
  fn = REGISTRY.get(command.command, None)
  if (fn):
    fn(command)

class Command(object):
  def __init__(self, req):
    self.token = req.get('token')
    self.team_id = req.get('team_id')
    self.channel_id = req.get('channel_id')
    self.channel_name = req.get('channel_name')
    self.user_id = req.get('user_id')
    self.user_name = req.get('user_name')
    self.command = req.get('command')
    self.text = req.get('text')
    self.req = req

def extract_entity(text):
  tokens = filter(None, re.split(r'\s+', text.lstrip(), maxsplit=1, flags=re.UNICODE))
  return tokens



def score(command, delta, message, icon_emoji):
  info = extract_entity(command.text)
  if info:
    r = entity.inc_entity(info[0], delta)

    line = message.format(
      to=info[0] + u'\u200E',
      score=r.score,
      reason='' if len(info) < 2 else ' ' + info[1]
    )

    logging.info(line)

    incoming_webhook.post(
      line,
      username=command.user_name,
      channel='#' + command.channel_name,
      icon_emoji=icon_emoji)


def plusplus(command):
  score(command, 1, u'{to}++ (now at {score}){reason}', ':thumbsup:')

def minusminus(command):
  score(command, -1, u'{to}-- (now at {score}){reason}', ':thumbsdown:')

register(u'/++', plusplus)
register(u'/--', minusminus)
# em-dash
register(u'/\u2014', minusminus)
