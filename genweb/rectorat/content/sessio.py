# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText


from genweb.rectorat import _


class ISessio(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """

    dataSessio = schema.Datetime(
        title=_(u"Data de la Sessió"),
        description=_(u"Data de la Sessió"),
        required=True,
    )

    llocConvocatoria = schema.TextLine(
        title=_(u"Lloc de la convocatòria"),
        description=_(u"Lloc de la convocatòria"),
        required=False,
    )

    horaIniciFi = schema.Datetime(
        title=_(u"Hora d'inici i de fi"),
        description=_(u"Hora d'inici i de fi"),
        required=False,
    )

    descripcioProposit = RichText(
        title=_(u"Descripció del Propòsit"),
        description=_(u"Descripció del propòsit de la sessió"),
        required=False,
    )

    membresConvocats = schema.Text(
        title=_(u"Membres convocats"),
        description=_(u"Membres convocats"),
        required=False,
    )

    llistaAssistents = schema.Text(
        title=_(u"Llista assistents"),
        description=_(u"Llista assistents"),
        required=False,
    )

    ordreSessio = RichText(
        title=_(u"Ordre de la Sessio"),
        description=_(u"Ordre de la Sessio"),
        required=False,
    )


class View(grok.View):
    grok.context(ISessio)
