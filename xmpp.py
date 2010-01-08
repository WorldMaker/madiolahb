# HCE Bee
# Copyright 2010 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from backend import COMMAND_RE, Commander
from channel import CHANNEL_RE
from hce import max_influence
from models import Channel
import waml

class XmppHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        channel = CHANNEL_RE.match(message.to)
        if not channel:
            self.error(404)
            return
        chan = Channel.get_by_key_name(channel.group())
        if not chan:
            self.error(404) # TODO: Send an error response?
            return
        self.receive(chan, message)

    def receive(self, channel, message):
        game = channel.active_email_game
        if not game: return
        com = Commander(game, message.sender)
        for match in COMMAND_RE.finditer(message.body):
            result = com.command(match.group('commands'))
            if any(sen['verb'] == 'act' or sen['verb'] == 'contest' for sen
            in com.commanded):
                message.reply(waml.plaintext('wave/roll.yaml', {
                    'roll': game.lastroll,
                }))
            if com.errors or com.warnings:
                message.reply(waml.plaintext('wave/errors.yaml', {
                    'errors': com.errors,
                    'warnings': com.warnings
                }))
            if com.tickselapsed:
                ticks = ''
                if com.tickselapsed <= 3:
                    ticks = ' '.join(['Tick.'] * com.tickselapsed)
                else:
                    ticks = '%s Ticks.' % com.tickselapsed
                message.reply(waml.plaintext('wave/ticks.yaml', {
                    'ticks': ticks, 'atready': com.atready, 
                    'maxpoise': max(max_influence(char, 'poise') for char \
                    in com.atready)
                }))
        com.commit()

application = webapp.WSGIApplication([
    ('/_ah/xmpp/message/chat/', XmppHandler),
])

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    template.register_template_library('templatetags')
    main()

# vim: ai et ts=4 sts=4 sw=4
