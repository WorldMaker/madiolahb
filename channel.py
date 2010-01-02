# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from gaejson import json
from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Channel, EmailGame, XmppGame
import re

CHANNEL_RE = re.compile(r'[a-z][a-z0-9\-]+')

class ChannelHomeHandler(webapp.RequestHandler):
    def get(self):
        mychans = Channel.all().filter('owner =', users.get_current_user())
        self.response.out.write(template.render('html/channels.html', {
            'channels': mychans,
        }))

class NewChannelHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('html/newchannel.html', {
            'valid': True,
            'available': True,
        }))

    def post(self):
        name = self.request.POST.get('name', '')
        valid = CHANNEL_RE.match(name) is not None
        avail = valid and Channel.get_by_key_name(name) is None
        if valid and avail:
            chan = Channel(key_name=name, owner=users.get_current_user())
            chan.put()
            self.redirect('/channel/edit/%s' % name)
            return
        self.response.out.write(template.render('html/newchannel.html', {
            'valid': valid,
            'available': avail,
        }))

class CheckChannelHandler(webapp.RequestHandler):
    def post(self):
        name = self.request.POST.get('name', '')
        valid = CHANNEL_RE.match(name) is not None
        data =  {
            'valid': valid,
            'available': valid and Channel.get_by_key_name(name) is None,
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))

class EditChannelHandler(webapp.RequestHandler):
    def get(self, channel=''):
        # TODO: Error Pages
        if not channel:
            self.error(404)
            return
        chan = Channel.get_by_key_name(channel)
        if not chan:
            self.error(404)
            return
        if chan.owner != users.get_current_user():
            self.error(403)
            return
        self.response.out.write(template.render('html/editchannel.html', {
            'channel': chan,
        }))

application = webapp.WSGIApplication([
    (r'/channel/new/?', NewChannelHandler),
    (r'/channel/available/?', CheckChannelHandler),
    (r'/channel/edit/(?P<channel>%s)/?' % CHANNEL_RE.pattern,
        EditChannelHandler),
    (r'/channel/?', ChannelHomeHandler),
])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    # template.register_template_library('templatetags')
    main()

# vim: ai et ts=4 sts=4 sw=4
