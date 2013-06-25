from google.appengine.ext import endpoints
from protorpc import messages
from protorpc import remote

from model import Contact


class EmptyRequest(messages.Message):
  pass


class IdMessage(messages.Message):
  id = messages.IntegerField(1, required=True)


# TODO implement the missing messages

# TODO add decorators to declare service
class ContactApi(remote.Service):

  # TODO add decorators to declare method
  def add(self, request):
    # TODO implement save
    pass

  # TODO add decorators to declare method
  def get(self, request):
    entity_id = request.id
    if not entity_id:
      message = 'Request should specify an id.' % entity_id
      raise endpoints.BadRequestException(message)

    entry = Contact.get_by_id(entity_id)
    
    if not entry:
      message = 'No entity with the id "%s" exists.' % entity_id
      raise endpoints.NotFoundException(message)

    return _BuildContactMessage(entry)

  # TODO implement list message
  def list(self, request):
    contact_messages = []
    for contact in Contact.query().fetch():
      # TODO pack contacts in response
    


def _BuildContactMessage(contact):
  return ContactMessage(id=contact.key.id(),
                       name=contact.name,
                       email=contact.email)


def _BuildContact(message):
  return Contact(id=message.id,
                 name=message.name,
                 email=message.email)


app = endpoints.api_server([ContactApi],
                           restricted=False)
