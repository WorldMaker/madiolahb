# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from gaejson import GaeEncoder, json
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Character, Game

class GameHandler(webapp.RequestHandler):
    def get(self, key):
        k = db.Key(key)
        if not k:
            self.error(404)
            return
        game = Game.get(k)
        if not game:
            self.error(404)
            return
        if self.request.GET.get('format', '') == 'json':
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(game, cls=GaeEncoder))
        else:
            self.response.out.write(template.render('html/game.html', {
                'game': game,
            }))

class CharHandler(webapp.RequestHandler):
    def get(self, key):
        k = db.Key(key)
        if not k:
            self.error(404)
            return
        char = Character.get(k)
        if not char:
            self.error(404)
            return
        if self.request.GET.get('format', '') == 'json':
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(char, cls=GaeEncoder))
        else:
            self.response.out.write(template.render('html/char.html', {
                'char': char,
            }))

application = webapp.WSGIApplication([
    (r'/game/([^/]+)/?', GameHandler),
    (r'/char/([^/]+)/?', CharHandler),
])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

# vim: ai et ts=4 sts=4 sw=4
