import unittest
import commands
import slack
from google.appengine.ext import testbed

class TestCommands(unittest.TestCase):

  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()


  def test_normalize_entity(self):
    self.assertEqual((u'', u''), commands.normalize_entity(u''))
    self.assertEqual((u'HI', u'hi'), commands.normalize_entity(u'HI,'))
    self.assertEqual((u'@johng', 'johng'), commands.normalize_entity(u'@johng'))
    self.assertEqual((u'caf\xe9', u'caf\xe9') , commands.normalize_entity(u'caf\xe9,'))

  def test_normalize_entities(self):
    text = u''
    expected = ([], u'')
    self.assertEqual(expected, commands.normalize_entities(text))

    text = u'@JohnG for fs-slack'
    expected = ([(u'@JohnG', u'johng')], u'for fs-slack')
    self.assertEqual(expected, commands.normalize_entities(text))

    text = u'@JohnG, @jorgeo for fs-slack'
    expected = ([(u'@JohnG', u'johng'), (u'@jorgeo',u'jorgeo')], u'for fs-slack')
    self.assertEqual(expected, commands.normalize_entities(text))

    text = u'@JohnG, @jorgeo'
    expected = ([(u'@JohnG', u'johng'), (u'@jorgeo',u'jorgeo')], u'')
    self.assertEqual(expected, commands.normalize_entities(text))

  def test_plusplus(self):
    slack_impl = slack.TestSlack()
    command = commands.Command({
        'text': u'@JohnG, @jorgeo for fs-slack',
        'channel_name': u'testchan'
    })
    expected = u'@JohnG\u200e++ (now at 1), @jorgeo\u200e++ (now at 1) for fs-slack'
    commands.plusplus(slack_impl, command)
    self.assertEqual(expected, slack_impl.last_payload['text'])

    # do it again
    expected = u'@JohnG\u200e++ (now at 2), @jorgeo\u200e++ (now at 2) for fs-slack'
    commands.plusplus(slack_impl, command)
    self.assertEqual(expected, slack_impl.last_payload['text'])

