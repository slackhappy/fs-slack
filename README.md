# fs-slack #

silly slash command synthesis for slack


## Supported commands ##
- `/++ thing[, thing2] [reason]`  increment thing's score
- `/-- thing[, thing2] [reason]`  decrement thing's score
- `/h` show the command help

## Installation ##
1. Deploy to appspot
2. Fill in /config with your [incoming webhook](https://foursquare.slack.com/services/new/incoming-webhook) token and domain
3. Add [slash commands](https://foursquare.slack.com/services/new/slash-commands) for all supported commands
4. For paste support, add an [api token](https://api.slack.com/) to /config
