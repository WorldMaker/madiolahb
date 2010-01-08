# HCE Bee
# Copyright 2010 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from backend import COMMAND_RE, Commander
from channel import CHANNEL_RE
from hce import max_influence
from models import Channel
import re
import waml

HCE_MAIL_RE = re.compile(r'^(hce-bee@appspot.com|.+@.*hce-bee.appspotmail.com)$')
RE_RE = re.compile(r'\s*([Rr][Ee]:|[Ff][Ww][Dd]:)')

class ChannelHandler(webapp.RequestHandler):
    def post(self, channel):
        chan = Channel.get_by_key_name(channel)
        if not chan:
            self.error(404) # TODO: Send an error email?
            return
        self.receive(chan, mail.InboundEmailMessage(self.request.body))

    def receive(self, channel, message):
        game = channel.active_email_game
        if not game: return
        com = Commander(game, message.sender)
        replies = []
        for body in message.bodies(content_type="text/plain"):
            for match in COMMAND_RE.finditer(body):
                result = com.command(match.group('commands'))
                if result is not False:
                    replies.append("(%s)" % match.group('commands'))
                if any(sen['verb'] == 'act' or sen['verb'] == 'contest' for sen
                in com.commanded):
                    replies.append(waml.plaintext('wave/roll.yaml', {
                        'roll': game.lastroll,
                    }))
                if com.errors or com.warnings:
                    replies.append(waml.plaintext('wave/errors.yaml', {
                        'errors': com.errors,
                        'warnings': com.warnings
                    }))
                if com.tickselapsed:
                    ticks = ''
                    if com.tickselapsed <= 3:
                        ticks = ' '.join(['Tick.'] * com.tickselapsed)
                    else:
                        ticks = '%s Ticks.' % com.tickselapsed
                    replies.append(waml.plaintext('wave/ticks.yaml', {
                        'ticks': ticks, 'atready': com.atready, 
                        'maxpoise': max(max_influence(char, 'poise') for char \
                        in com.atready)
                    }))
        reply = mail.EmailMessage()
        reply.sender='HCE Bee <%s@hce-bee.appspotmail.com>' % channel.key().name()
        reply.subject = message.subject
        if not RE_RE.match(subject):
            reply.subject = "RE: " + reply.subject
        to = [addr for addr in message.to if HCE_MAIL_RE.match(addr) is None]
        cc = [addr for addr in message.cc if HCE_MAIL_RE.match(addr) is None]
        if message.sender not in to:
            to.append(message.sender)
        reply.to = to
        reply.cc = cc
        reply.body = '\n\n'.join(replies)
        reply.send()
        com.commit()

application = webapp.WSGIApplication([
    ('/_ah/mail/(?P<channel>%s)@.+' % CHANNEL_RE.pattern, ChannelHandler),
])

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    template.register_template_library('templatetags')
    main()

# vim: ai et ts=4 sts=4 sw=4
