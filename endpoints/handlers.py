import main

import jinja2
import os
import webapp2

class MainHandler(webapp2.RequestHandler):

  def _render_template(self, template_values):
    template = main.jinja_environment.get_template(
        os.path.join('endpoints', 'index.html'))
    self.response.out.write(template.render(template_values))

  def get(self):
    self._render_template({})
