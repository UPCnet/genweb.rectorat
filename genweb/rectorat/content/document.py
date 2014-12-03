# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText
from genweb.rectorat import _
from plone.namedfile.field import NamedFile
from plone.app.dexterity import PloneMessageFactory as _PMF

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form as directivesform
from plone.formwidget.multifile import MultiFileFieldWidget
from plone.namedfile.field import NamedFile
from zope.interface import Interface


estats = SimpleVocabulary(
    [SimpleTerm(value=u'Esborrany', title=_(u'Esborrany')),
     SimpleTerm(value=u'Pendent', title=_(u'Pendent')),
     SimpleTerm(value=u'Aprovat', title=_(u'Aprovat')),
     SimpleTerm(value=u'Rebutjat', title=_(u'Rebutjat')),
     ]
    )


class IDocument(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """

    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    descripcioProposit = RichText(
        title=_(u"Proposal description"),
        required=False,
    )

    proposalPoint = schema.TextLine(
        title=_(u'Proposal point number'),
        required=False
    )

    numDoc = schema.TextLine(
        title=_(u'Document number'),
        required=False
    )

    estatAprovacio = schema.Choice(
        title=_(u"Approval status"),
        vocabulary=estats,
        default='Esborrany',
    )

    comentariEstatAprovacio = RichText(
        title=_(u"Approval status comment"),
        required=False,
    )

    directivesform.widget(fitxersOriginal=MultiFileFieldWidget)
    fitxersOriginal = schema.List(title=_(u"Original files"),
                                  value_type=NamedFile())

    directivesform.widget(fitxersPerPublicar=MultiFileFieldWidget)
    fitxersPerPublicar = schema.List(title=_(u"Published files"),
                                     value_type=NamedFile())


class View(grok.View):
    grok.context(IDocument)
    grok.template('document_view')
