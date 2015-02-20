from zope.interface import implements
from plone.dexterity.content import Item

from genweb.rectorat.content.sessio import ISessio
from genweb.rectorat.content.organgovern import IOrgangovern
from genweb.rectorat.content.document import IDocument
from genweb.rectorat.content.acta import IActa


class Sessio(Item):
    implements(ISessio)


class Organgovern(Item):
    implements(IOrgangovern)


class Document(Item):
    implements(IDocument)


class Acta(Item):
    implements(IActa)
