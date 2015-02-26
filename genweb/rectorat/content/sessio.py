# -*- coding: utf-8 -*-
import datetime
from five import grok
from zope import schema
from plone import api


from plone.directives import dexterity
from plone.directives import form
from plone.app.textfield import RichText
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE

from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF
from collective import dexteritytextindexer
from Products.CMFCore.utils import getToolByName


class InvalidEmailError(schema.ValidationError):
    __doc__ = u'Please enter a valid e-mail address.'


class ISessio(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    dataSessio = schema.Date(
        title=_(u"Session date"),
        required=True,
    )

    llocConvocatoria = schema.TextLine(
        title=_(u"Session place"),
        required=False,
    )

    horaInici = schema.Time(
        title=_(u"Session start time"),
        required=False,
    )

    horaFi = schema.Time(
        title=_(u"Session end time"),
        required=False,
    )

    adrecaLlista = schema.Text(
        title=_(u"mail address"),
        description=_(u"Enter email lists adresses, separated by commas."),
        required=True,
    )

    dexteritytextindexer.searchable('membresConvocats')
    membresConvocats = RichText(
        title=_(u"Incoming members list"),
        required=False,
    )

    dexteritytextindexer.searchable('membresConvidats')
    membresConvidats = RichText(
        title=_(u"Invited members"),
        required=False,
    )

    dexteritytextindexer.searchable('llistaExcusats')
    llistaExcusats = RichText(
        title=_(u"Excused members"),
        required=False,
    )

    dexteritytextindexer.searchable('ordreSessio')
    ordreSessio = RichText(
        title=_(u"Session order"),
        required=False,
    )

    dexteritytextindexer.searchable('bodyMail')
    bodyMail = RichText(
        title=_(u"Body Mail"),
        description=_(u"Body Mail description"),
        required=False,
    )

    form.mode(notificationDate='hidden')
    notificationDate = schema.TextLine(
        title=_(u"Notification date"),
        required=False,
    )


@form.default_value(field=ISessio['dataSessio'])
def dataSessioDefaultValue(data):
    return datetime.datetime.today()


@form.default_value(field=ISessio['horaInici'])
def horaIniciDefaultValue(data):
    time = datetime.datetime.today()
    return time


@form.default_value(field=ISessio['horaFi'])
def horaFiDefaultValue(data):
    time = datetime.datetime.today() + datetime.timedelta(hours=1)
    return time


@form.default_value(field=ISessio['membresConvocats'])
def membresConvocatsDefaultValue(data):
    # copy members from Organ de Govern (parent object)
    return data.context.membresOrgan


@form.default_value(field=ISessio['adrecaLlista'])
def adrecaLlistaDefaultValue(data):
    # copy adrecaLlista from Organ de Govern (parent object)
    return data.context.adrecaLlista


class View(grok.View):
    grok.context(ISessio)
    grok.template('sessio_view')

    def isAuthenticated(self):
        if api.user.is_anonymous():
            return False
        else:
            return True

    def DocumentsInside(self):
        """ Retorna els documents creats aquí dintre (sense tenir compte estat)
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        # Cerca contingut per mostar al carousel en diversos idiomes
        folder_path = '/'.join(self.context.getPhysicalPath())

        data = portal_catalog.searchResults(portal_type='genweb.rectorat.document',
                                            path={'query': folder_path,
                                                  'depth': 1})

        return data

    def ActasInside(self):
        """ Retorna les actes creades aquí dintre (sense tenir compte estat)
        """
        folder_path = '/'.join(self.context.getPhysicalPath())
        portal_catalog = getToolByName(self, 'portal_catalog')
        data = portal_catalog.searchResults(portal_type='genweb.rectorat.acta',
                                            path={'query': folder_path,
                                                  'depth': 1})
        return data


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(ISessio)

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        self.widgets['notificationDate'].mode = HIDDEN_MODE
