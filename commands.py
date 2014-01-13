import api
import entity
import incoming_webhook
import logging
import re


REGISTRY = {}

def register(name, fn, help_text=None):
  global REGISTRY
  REGISTRY[name] = (fn, help_text)

def run(req):
  command = Command(req)
  fn, help_text = REGISTRY.get(command.command, (None, None))
  if (fn):
    return fn(command)

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

def do_paste(command, content, filetype='text'):
  api.files_upload(
    content=content,
    filetype=filetype,
    title=command.user_name + ' pasted some text',
    channels=[command.channel_id])

def paste(command):
  info = extract_entity(command.text)
  filetype = 'text'
  content = command.text

  if len(info) > 1 and info[0] in ['scala', 'python']:
    filetype = info[0]
    content = info[1]
  do_paste(command, content, filetype)

def pscala(command):
  do_paste(command, command.text, 'scala')

def h(command):
  logging.info('hi')
  response = u'fs-slack commands:\n'
  for key in sorted(REGISTRY.keys()):
    fn, help_text = REGISTRY[key]
    response += u'{0} {1}\n'.format(key, '' if not help_text else help_text)
  response += '\nrun /help commands for official slack commands\n'
  return response



register(u'/++', plusplus, 'thing [reason]\t\t\t\t\t\tincrement score of thing [for reason]')
register(u'/--', minusminus, 'thing [reason]\t\t\t\t\t\tdecrement score of thing [for reason]')
# em-dash
register(u'/\u2014', minusminus, 'thing [reason]\t\t\t\t\t\tdecrement score of thing [for reason]')

register(u'/p', paste, '[scala|python] some text\t\tpaste some text [optionally set language]')
register(u'/pscala', pscala, 'some text\t\t\t\t\tpaste some text in scala')
register(u'/h', h, '\t\t\t\t\t\t\t\t\t\t\tthis help message')
