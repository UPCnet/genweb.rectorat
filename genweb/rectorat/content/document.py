# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from plone.directives import dexterity
from plone.app.textfield import RichText
from plone.namedfile.field import NamedFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form as directivesform
from plone.formwidget.multifile import MultiFileFieldWidget
from z3c.form.interfaces import DISPLAY_MODE, HIDDEN_MODE

from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF

estats = SimpleVocabulary(
    [SimpleTerm(value='Draft', title=_(u'Draft')),
     SimpleTerm(value='Pending', title=_(u'Pending')),
     SimpleTerm(value='Approved', title=_(u'Approved')),
     SimpleTerm(value='Rejected', title=_(u'Rejected')),
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

    proposalPoint = schema.TextLine(
        title=_(u'Proposal point number'),
        required=False
    )

    numDoc = schema.TextLine(
        title=_(u'Document number'),
        required=False
    )

    descripcioProposit = RichText(
        title=_(u"Proposal description"),
        required=False,
    )

    estatAprovacio = schema.Choice(
        title=_(u"Approval status"),
        vocabulary=estats,
        default=_(u'Draft'),
    )

    comentariEstatAprovacio = RichText(
        title=_(u"Approval status comment"),
        required=False,
    )

    directivesform.widget(fitxersOriginal=MultiFileFieldWidget)
    fitxersOriginal = schema.List(title=_(u"Original files"),
                                  value_type=NamedFile(),
                                  required=False,)

    directivesform.widget(fitxersPerPublicar=MultiFileFieldWidget)
    fitxersPerPublicar = schema.List(title=_(u"Published files"),
                                     value_type=NamedFile(),
                                     required=False,)

    form.mode(notificationDate='hidden')
    notificationDate = schema.TextLine(
        title=_(u"Notification date"),
        required=False,
    )


class View(dexterity.DisplayForm):
    grok.context(IDocument)
    grok.template('document_view')


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(IDocument)

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        #self.widgets['notificationDate'].mode = 'hidden'
        self.widgets['notificationDate'].mode = DISPLAY_MODE
