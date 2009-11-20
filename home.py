from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class HomeHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('/docs/index.html')

application = webapp.WSGIApplication([
    (r'/', HomeHandler),
])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

# vim: ai et ts=4 sts=4 sw=4
