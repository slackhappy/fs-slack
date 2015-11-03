import api
import entity_db
import logging
import re


REGISTRY = {}

def register(name, fn, help_text=None):
  global REGISTRY
  REGISTRY[name] = (fn, help_text)

def run(slack_impl, req):
  command = Command(req)
  fn, help_text = REGISTRY.get(command.command, (None, None))
  if fn:
    return fn(slack_impl, command)

class Command(object):
  def __init__(self, req):
    self.channel_id = req.get('channel_id')
    self.channel_name = req.get('channel_name')
    self.user_id = req.get('user_id')
    self.user_name = req.get('user_name')
    self.command = unicode(req.get('command'))
    self.text = unicode(req.get('text'))
    self.req = req

def extract_entity(text):
  tokens = filter(None, re.split(r'\s+', text.lstrip(), maxsplit=1, flags=re.UNICODE))
  return tokens

def normalize_entity(entity_text):
  if not entity_text:
    return (entity_text, entity_text)

  if entity_text[-1] == u',':
    entity_text = entity_text[:-1]

  entity = entity_text.lower()
  if entity[0] == u'@':
    entity = entity[1:]
  return (entity_text, entity)

def normalize_entities(text):
  extract_again = len(text) > 0
  entities = []
  while extract_again:
    parts = extract_entity(text)
    # trailing comma indicates more than one entity to extract
    extract_again = len(parts) > 1 and parts[0].endswith(',')
    if len(parts) > 0:
      entity = parts[0]
      (entity, normalized_entity) = normalize_entity(entity)
      if entity:
        entities.append((entity, normalized_entity))
    if len(parts) > 1:
      text = parts[1]
    else:
      text = u''

  return (entities, text)



def score(slack_impl, command, delta, message, icon_emoji):
  (entities, rest) = normalize_entities(command.text)
  if entities:
    messages = []

    for (entity, normalized_entity) in entities:
      r = entity_db.inc_entity(normalized_entity, delta)
      messages.append(message.format(
          to=(entity + u'\u200E'), # 200E is LTR
          score=r.score))

    line = ' '.join([
        u', '.join(messages),
        rest
    ])

    logging.info(line)

    slack_impl.post(
        line,
        username=command.user_name,
        channel=command.channel_id,
        icon_emoji=icon_emoji)


def plusplus(slack_impl, command):
  score(slack_impl, command, 1, u'{to}++ (now at {score})', ':thumbsup:')

def minusminus(slack_impl, command):
  score(slack_impl, command, -1, u'{to}-- (now at {score})', ':thumbsdown:')

def h(slack_impl, command):
  logging.info('hi')
  response = u'fs-slack commands:\n'
  for key in sorted(REGISTRY.keys()):
    fn, help_text = REGISTRY[key]
    response += u'{0} {1}\n'.format(key, '' if not help_text else help_text)
  response += '\nrun /help commands for official slack commands\n'
  return response



register(u'/++', plusplus, 'thing[, thing2]  [reason]\t\t\t\t\t\tincrement score of thing[, thing2] [for reason]')
register(u'/--', minusminus, 'thing[, thing2] [reason]\t\t\t\t\t\tdecrement score of thing[, thing2][for reason]')
# em-dash
register(u'/\u2014', minusminus, 'thing[, thing2] [reason]\t\t\t\t\t\tdecrement score of thing[, thing2] [for reason]')

register(u'/h', h, '\t\t\t\t\t\t\t\t\t\t\tthis help message')
