# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText
from genweb.rectorat import _
from plone.namedfile.field import NamedFile

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

estats = SimpleVocabulary(
    [SimpleTerm(value=u'Esborrany', title=_(u'Esborrany')),
     SimpleTerm(value=u'Pendent', title=_(u'Pendent')),
     SimpleTerm(value=u'Aprovat', title=_(u'Aprovat')),
     SimpleTerm(value=u'No aprovat', title=_(u'No aprovat')),
     ]
    )


class IDocument(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """

    descripcioProposit = RichText(
        title=_(u"Descripció del Propòsit"),
        description=_(u"Descripció del propòsit de la sessió"),
        required=False,
    )

    estatAprovacio = schema.Choice(
        title=_(u"Estat Aprovació"),
        description=_(u"Estat Aprovació"),
        vocabulary=estats,
        default='Esborrany',
    )

    comentariEstatAprovacio = RichText(
        title=_(u"Comentari a l'estat d'aprovació"),
        description=_(u"Comentari a l'estat d'aprovació"),
        required=False,
    )

    fitxer = NamedFile(
        title=_(u"Annex amb el fitxer original"),
        description=_(u"Annex amb el fitxer original"),
        required=False,
    )


class View(grok.View):
    grok.context(IDocument)
    grok.template('document_view')
