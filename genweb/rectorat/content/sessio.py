# -*- coding: utf-8 -*-
import datetime
from five import grok
from zope import schema
from plone import api

from Products.CMFCore.utils import getToolByName
from plone.directives import dexterity
from plone.directives import form
from plone.app.textfield import RichText
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE

from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF


class InvalidEmailError(schema.ValidationError):
    __doc__ = u'Please enter a valid e-mail address.'


class ISessio(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """

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

    # descripcioProposit = RichText(
    #     title=_(u"Proposal description"),
    #     required=False,
    # )

    membresConvocats = schema.Text(
        title=_(u"Incoming members list"),
        required=False,
    )

    llistaAssistents = schema.Text(
        title=_(u"Invited members"),
        required=False,
    )

    llistaExcusats = schema.Text(
        title=_(u"Excused members"),
        required=False,
    )

    ordreSessio = RichText(
        title=_(u"Session order"),
        description=_(u"This content is not visible by anonymous"),
        required=False,
    )

    publishContent = schema.Bool(
        title=u'Mark this option to make publish content visible',
        description=_(u"By default, only published will be visible"),
        required=False,
        default=True,
    )

    contentPublished = RichText(
        title=_(u"Published content"),
        description=_(u"This content will be visible if the previous mark is enabled"),
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


class View(grok.View):
    grok.context(ISessio)
    grok.template('sessio_view')

    def getLang(self):
        wf_state = api.content.get_state(obj=self.context)
        lang = getToolByName(self, 'portal_languages').getPreferredLanguage()

        if wf_state == 'preparing':
            if lang == 'ca':
                return 'En preparació'
            if lang == 'es':
                return 'En preparación'
            if lang == 'en':
                return 'Preparing'

        if wf_state == 'convocat':
            return 'Convocada'

        if wf_state == 'closed':
            if lang == 'ca':
                return 'Tancada'
            if lang == 'es':
                return 'Cerrada'
            if lang == 'en':
                return 'Closed'

    def nextState(self):
        wf_state = api.content.get_state(obj=self.context)
        states = {'current': '', 'next': ''}
        if wf_state == 'preparing':
            states['current'] = 'preparing'
            states['next'] = 'convocat'
        if wf_state == 'convocat':
            states['current'] = 'convocat'
            states['next'] = 'closed'
        if wf_state == 'closed':
            states['current'] = 'closed'
            states['next'] = 'preparing'
        return states




class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(ISessio)

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        self.widgets['notificationDate'].mode = DISPLAY_MODE
