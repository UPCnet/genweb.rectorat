# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.namedfile.field import NamedFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.formwidget.multifile import MultiFileFieldWidget
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import dexterity
from plone.directives import form
from zope.interface import alsoProvides

from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.supermodel import model
from z3c.form.interfaces import INPUT_MODE, DISPLAY_MODE, HIDDEN_MODE
from plone import api
from collective import dexteritytextindexer
from plone.indexer.decorator import indexer


estats = SimpleVocabulary(
    [SimpleTerm(value='Draft', title=_(u'Draft')),
     SimpleTerm(value='Informed', title=_(u'Informed')),
     SimpleTerm(value='Approved', title=_(u'Approved')),
     SimpleTerm(value='Rejected', title=_(u'Rejected')),
     SimpleTerm(value='Pending', title=_(u'Pending')),
     ]
    )


class IDocument(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    proposalPoint = schema.TextLine(
        title=_(u'Proposal point number'),
        required=False
    )

    agreement = schema.TextLine(
        title=_(u'Agreement number'),
        required=False
    )

    dexteritytextindexer.searchable('defaultContent')
    defaultContent = RichText(
        title=_(u"Proposal description"),
        description=_(u"Default content shown in the document view"),
        required=False,
    )

    dexteritytextindexer.searchable('alternateContent')
    alternateContent = RichText(
        title=_(u"Alternate description"),
        description=_(u"Content used to hide protected content"),
        required=False,
    )

    estatAprovacio = schema.Choice(
        title=_(u"Approval status"),
        vocabulary=estats,
        default=_(u'Draft'),
    )

    dexteritytextindexer.searchable('comentariEstatAprovacio')
    comentariEstatAprovacio = RichText(
        title=_(u"Approval status comment"),
        required=False,
    )

    dexteritytextindexer.searchable('PublishedFiles')
    form.widget(PublishedFiles=MultiFileFieldWidget)
    PublishedFiles = schema.List(title=_(u"Published files"),
                                 description=_(u"Published files description"),
                                 value_type=NamedFile(),
                                 required=False,)

    dexteritytextindexer.searchable('OriginalFiles')
    form.widget(OriginalFiles=MultiFileFieldWidget)
    OriginalFiles = schema.List(title=_(u"Original files"),
                                description=_(u"Original files description"),
                                value_type=NamedFile(),
                                required=False,)

alsoProvides(IDocument, IFormFieldProvider)


class View(dexterity.DisplayForm):
    grok.context(IDocument)
    grok.template('document_view')

    def isAuthenticated(self):
        if api.user.is_anonymous():
            return False
        else:
            return True


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(IDocument)

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        self.widgets['estatAprovacio'].mode = INPUT_MODE
