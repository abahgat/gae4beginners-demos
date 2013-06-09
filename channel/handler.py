import main

import jinja2
import os
import json
import uuid
import webapp2

from google.appengine.api import channel
from google.appengine.api import memcache

class CursorHandler(webapp2.RequestHandler):

  def _render_template(self, template_values):
    template = main.jinja_environment.get_template(
        os.path.join('channel', 'index.html'))
    self.response.out.write(template.render(template_values))

  def get(self):
    client_id = uuid.uuid4().hex

    token = channel.create_channel(client_id)

    template_values = {
      'client': client_id,
      'token': token
    }
    self._render_template(template_values)

  def post(self):
    x = self.request.get('x')
    y = self.request.get('y')
    client_id = self.request.get('client')

    message = {
      'type': 'move',
      'client': client_id,
      'x': x,
      'y': y,
    }

    clients = memcache.get('clients')
    if clients:
      for client in clients:
        channel.send_message(client, json.dumps(message))

class ConnectHandler(webapp2.RequestHandler):
  """Handler that will be called when a new client connects."""

  def post(self):
    client_id = self.request.get('from')

    clients = memcache.get('clients')
    if clients is None:
      clients = set([client_id])
    else:
      clients.add(client_id)

    memcache.set('clients', clients)

class DisconnectHandler(webapp2.RequestHandler):
  """Handler that will be called when a client disconnects."""

  def post(self):
    client_id = self.request.get('from')

    clients = memcache.get('clients')
    if clients is None:
      return None

    clients.remove(client_id)
    memcache.set('clients', clients)

    message = {
      'type': 'disconnect',
      'client': client_id,
    }
    for client in clients:
        channel.send_message(client, json.dumps(message))
