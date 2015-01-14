# -*- coding: utf-8 -*-
import re
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText
from plone import api

from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF

EMAIL_RE = u"([0-9a-zA-Z_&.'+-]+!)*[0-9a-zA-Z_&.'+-]+@(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"


class InvalidEmailError(schema.ValidationError):
    __doc__ = _(u"Invalid email address")


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
        title=_(u"Organ Govern description"),
        required=False,
    )

    adrecaLlista = schema.Text(
        title=_(u"mail address"),
        description=_(u"Enter email lists adresses, separated by commas."),
        required=False,
    )

    membresOrgan = schema.Text(
        title=_(u"Organ Govern members"),
        description=_(u"Indicar el nom dels assistents separats per comes"),
        required=False,
    )

    fromMail = schema.TextLine(
        title=_(u'From mail'),
        description=_(u'Enter the from used in the mail form'),
        required=False
    )


class View(grok.View):
    grok.context(IOrgangovern)
    grok.template('organgovern_view')

    def getSeparatedMembers(form):
        # TODO: Return members separated by comma
        return None

    def isAuthenticated(self):
        # Check if user has admin role to show the bottom information box
        # (only for managers)
        if api.user.is_anonymous():
            # is anon
            canViewContent = False
        else:
            # # Is a validated user...
            # username = api.user.get_current().getProperty('id')
            # # get username
            # roles = api.user.get_roles(username=username)
            # # And check roles
            # if 'Editor' in roles or 'Manager' in roles:
            #     canViewContent = True
            # else:
            #     canViewContent = False

            # All validated users can view this
            canViewContent = True
        return canViewContent
