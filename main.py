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
    # TODO here's where you should map your URLs
], debug=True)
