# -*- coding: utf-8 -*-
import datetime
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText
from plone.app.dexterity import PloneMessageFactory as _PMF

from genweb.rectorat import _


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

    form.omitted('description')
    description = schema.Text(
        title=_PMF(u'label_description', default=u'Summary'),
        description=_PMF(
            u'help_description',
            default=u'Used in item listings and search results.'
        ),
        required=False,
        missing_value=u'',
    )

    dataSessio = schema.Datetime(
        title=_(u"Data de la Sessió"),
        # description=_(u"Data de la Sessió"),
        required=True,
    )

    llocConvocatoria = schema.TextLine(
        title=_(u"Lloc de la convocatòria"),
        # description=_(u"Lloc de la convocatòria"),
        required=False,
    )

    horaInici = schema.Time(
        title=_(u"Hora d'inici de la Sessió"),
        # description=_(u"Hora d'inici de la Sessió"),
        required=False,
    )

    horaFi = schema.Time(
        title=_(u"Hora de fi de la Sessió"),
        # description=_(u"Hora de fi de la Sessió"),
        required=False,
    )

    descripcioProposit = RichText(
        title=_(u"Descripció del Propòsit"),
        # description=_(u"Descripció del propòsit de la sessió"),
        required=False,
    )

    membresConvocats = schema.Text(
        title=_(u"Membres convocats"),
        # description=_(u"Membres convocats"),
        required=False,
    )

    llistaAssistents = schema.Text(
        title=_(u"Llista assistents"),
        # description=_(u"Llista assistents"),
        required=False,
    )

    ordreSessio = RichText(
        title=_(u"Ordre de la Sessio"),
        # description=_(u"Ordre de la Sessio"),
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


class View(grok.View):
    grok.context(ISessio)
    grok.template('sessio_view')
