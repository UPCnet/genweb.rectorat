from zope.interface import implements
from plone.dexterity.content import Item

from genweb.rectorat.content.sessio import ISessio


class Sessio(Item):
    implements(ISessio)
