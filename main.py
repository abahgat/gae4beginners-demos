import jinja2
import os
import webapp2

class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('Hello world!')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/channel', 'channel.handlers.CursorHandler'),
    ('/_ah/channel/connected/', 'channel.handlers.ConnectHandler'),
    ('/_ah/channel/disconnected/', 'channel.handlers.DisconnectHandler'),
], debug=True)
