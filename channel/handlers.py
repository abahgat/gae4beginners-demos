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

    # TODO create a channel and supply the id and token to the client
    pass
    
    self._render_template(template_values)

  def post(self):
    """This is where the client will send us messages with the coordinates of the mouse cursor."""
    # TODO unpack coordinates
    
    # TODO pack message for clients

    # TODO send a message to each connected client
    pass

class ConnectHandler(webapp2.RequestHandler):
  """Handler that will be called when a new client connects."""

  def post(self):
    # TODO add this client to the list of known clients
    # start from this: client_id = self.request.get('from')
    pass

class DisconnectHandler(webapp2.RequestHandler):
  """Handler that will be called when a client disconnects."""

  def post(self):
    # TODO forget about this client
    # client_id = self.request.get('from')

    # TODO notify clients of disappearance ;)
    pass
