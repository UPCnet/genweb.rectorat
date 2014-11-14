from zope.interface import implements
from plone.dexterity.content import Item

from genweb.rectorat.content.sessio import ISessio
from genweb.rectorat.content.organgovern import IOrgangovern


class Sessio(Item):
    implements(ISessio)


class Organgovern(Item):
    implements(IOrgangovern)
