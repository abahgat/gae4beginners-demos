import main

import jinja2
import os
import json
import uuid
import webapp2

from google.appengine.api import channel

class CursorHandler(webapp2.RequestHandler):
  def get(self):
    client_id = uuid.uuid4().hex

    token = channel.create_channel(client_id)

    template_values = {
      'client_id': client_id,
      'token': token
    }
    template = main.jinja_environment.get_template(
        os.path.join('channel', 'index.html'))
    self.response.out.write(template.render(template_values))

  def post(self):
    x = self.request.get('x')
    y = self.request.get('y')
    client_id = self.request.get('client_id')

    message = {
      'x': x,
      'y': y,
      'client': client_id,
    }
    channel.send_message(client_id, json.dumps(message))