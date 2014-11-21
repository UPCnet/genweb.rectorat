# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText
from genweb.rectorat import _
from plone.namedfile.field import NamedFile
from plone.app.dexterity import PloneMessageFactory as _PMF

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

    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    descripcioProposit = RichText(
        title=_(u"Proposal description"),
        required=False,
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

    fitxer = NamedFile(
        title=_(u"Original file annex"),
        required=False,
    )

    def getFileInfo(context):
        from Products.CMFDefault.utils import decode

        options = {}
        options['title'] = context.Title()
        options['description'] = context.Description()
        options['content_type'] = context.getContentType()
        options['id'] = context.getId()
        options['size'] = context.get_size()
        options['url'] = context.absolute_url()

        return context.file_view_template(**decode(options))


class View(grok.View):
    grok.context(IDocument)
    grok.template('document_view')
