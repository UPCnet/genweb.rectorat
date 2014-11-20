# -*- coding: utf-8 -*-
import re
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText
from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF

EMAIL_RE = u"([0-9a-zA-Z_&.'+-]+!)*[0-9a-zA-Z_&.'+-]+@(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"


class InvalidEmailError(schema.ValidationError):
    __doc__ = u'Cal introduïr una adreça de correu vàlida'


def isEmail(value):
    if re.match('^'+EMAIL_RE, value):
        return True
    raise InvalidEmailError


class IOrgangovern(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """

    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    descripcioOrgan = RichText(
        title=_(u"Descripció de l'Òrgan de Govern"),
        # description=_(u"Descripció de l'Òrgan de Govern"),
        required=False,
    )

    adrecaLlista = schema.TextLine(
        title=_(u"Adreça de la llista de distribució"),
        # description=_(u"Adreça de la llista de distribució"),
        constraint=isEmail,
        required=False,
    )

    membresOrgan = schema.Text(
        title=_(u"Membres de l'Òrgan de Govern"),
        description=_(u"Indicar el nom dels assistents separats per comes"),
        required=False,
    )



class View(grok.View):
    grok.context(IOrgangovern)
    grok.template('organgovern_view')
