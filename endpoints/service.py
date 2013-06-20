from google.appengine.ext import endpoints
from protorpc import messages
from protorpc import remote

from model import Contact


class EmptyRequest(messages.Message):
  pass


class IdMessage(messages.Message):
  id = messages.IntegerField(1, required=True)


class ContactMessage(messages.Message):
  # id is not required for new entries
  id = messages.IntegerField(1, required=False)
  name = messages.StringField(2, required=True)
  email = messages.StringField(3, required=True)


class GetContactsResponse(messages.Message):
  contacts = messages.MessageField(ContactMessage, 1, repeated=True)


@endpoints.api(name='addressbook',version='v1',
               description='A simple API to manage your address book')
class ContactApi(remote.Service):

  @endpoints.method(ContactMessage,
                    IdMessage,
                    path='contact',
                    name='add.contact',
                    http_method='POST')
  def add(self, request):
    contact = _BuildContact(request)
    contact.put()
    return IdMessage(id=contact.key.id())

  @endpoints.method(IdMessage,
                    ContactMessage,
                    path='contact',
                    name='get.contact',
                    http_method='GET')
  def get(self, request):
    #TODO(abahgat): would this work with placeholders? /_ah/spi/contacts/entity_id
    entity_id = request.id
    if not entity_id:
      message = 'Request should specify an id.' % entity_id
      raise endpoints.BadRequestException(message)

    entry = Contact.get_by_id(entity_id)
    
    if not entry:
      message = 'No entity with the id "%s" exists.' % entity_id
      raise endpoints.NotFoundException(message)

    return _BuildContactMessage(entry)

  @endpoints.method(EmptyRequest,
                    GetContactsResponse,
                    path='contacts',
                    name='get.contacts',
                    http_method='GET')
  def list(self, request):
    contact_messages = []
    for contact in Contact.query().fetch():
      contact_messages.append(_BuildContactMessage(contact))
    return GetContactsResponse(contacts=contact_messages)


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
