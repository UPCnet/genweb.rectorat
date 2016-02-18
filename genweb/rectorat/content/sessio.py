# -*- coding: utf-8 -*-
import datetime
from five import grok
from zope import schema
from plone import api
import re

from plone.indexer import indexer
from plone.directives import dexterity
from plone.directives import form
from plone.app.textfield import RichText
from zope.annotation.interfaces import IAnnotations

from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF
from collective import dexteritytextindexer
from Products.CMFCore.utils import getToolByName
from genweb.rectorat import utils


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

    dexteritytextindexer.searchable('signatura')
    signatura = RichText(
        title=_(u"Signatura"),
        description=_(u"Signatura description"),
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

    def isEditor(self):
        """ Show send message button if user is editor """
        return utils.isEditor(self)

    def isReader(self):
        return utils.isReader(self)

    def DocumentsInside(self):
        """ Retorna els documents creats aquí dintre (sense tenir compte estat)
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        # Cerca contingut per mostar al carousel en diversos idiomes
        folder_path = '/'.join(self.context.getPhysicalPath())

        data = portal_catalog.searchResults(portal_type='genweb.rectorat.document',
                                            sort_on='getObjPositionInParent',
                                            path={'query': folder_path,
                                                  'depth': 1})

        return data

    def ActasInside(self):
        """ Retorna les actes creades aquí dintre (sense tenir compte estat)
        """
        folder_path = '/'.join(self.context.getPhysicalPath())
        portal_catalog = getToolByName(self, 'portal_catalog')
        data = portal_catalog.searchResults(portal_type='genweb.rectorat.acta',
                                            sort_on='getObjPositionInParent',
                                            path={'query': folder_path,
                                                  'depth': 1})
        return data

    def OrganMail(self):
        """ Retorna mails de l'organ
        """
        # coger gente campo from del organ
        try:
            return self.context.aq_parent.adrecaLlista
        except:
            return None

    def LogInformation(self):
        """ Obtain annotations send mail :)
        """

        if api.user.is_anonymous():
            return False
        else:
            annotations = IAnnotations(self.context)
            # This is used to remove log entries manually
            # import ipdb;ipdb.set_trace()
            # aaa = annotations['genweb.rectorat.logMail']
            # pp(aaa)       # Search the desired entry position
            # aaa.pop(0)    # remove the entry
            # annotations['genweb.rectorat.logMail'] = aaa
            try:
                return sorted(annotations['genweb.rectorat.logMail'], reverse=True)
            except:
                return False


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(ISessio)


@indexer(ISessio)
def dataSessio(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``dataSessio`` value count it and index.
    """
    return context.dataSessio
grok.global_adapter(dataSessio, name='start')
