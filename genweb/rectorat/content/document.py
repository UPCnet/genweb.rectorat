# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.autoform import directives as form
from plone.supermodel import model

from plone.app.textfield import RichText
from plone.namedfile.field import NamedFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.directives import form as directivesform
from plone.formwidget.multifile import MultiFileFieldWidget

from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF

estats = SimpleVocabulary(
    [SimpleTerm(value='Draft', title=_(u'Draft')),
     SimpleTerm(value='Pending', title=_(u'Pending')),
     SimpleTerm(value='Approved', title=_(u'Approved')),
     SimpleTerm(value='Rejected', title=_(u'Rejected')),
     ]
    )


class IDocument(model.Schema):
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

    agreement = schema.TextLine(
        title=_(u'Agreement number'),
        required=False
    )

    defaultContent = RichText(
        title=_(u"Proposal description"),
        description=_(u"Default content shown in the document view"),
        required=False,
    )

    choicedContent = schema.Bool(
        title=_(u'Mark this option to make alternate content visible'),
        description=_(u"By default, only default content will be visible, not the alternate content"),
        required=False,
        default=False,
    )

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

    comentariEstatAprovacio = RichText(
        title=_(u"Approval status comment"),
        required=False,
    )

    form.read_permission(fitxersOriginal='cmf.ReviewPortalContent')
    form.write_permission(fitxersOriginal='cmf.ReviewPortalContent')
    directivesform.widget(fitxersOriginal=MultiFileFieldWidget)
    fitxersOriginal = schema.List(title=_(u"Original files"),
                                  value_type=NamedFile(),
                                  required=False,)
    
    form.read_permission(fitxersOriginal='cmf.ReviewPortalContent')
    form.write_permission(fitxersOriginal='cmf.ReviewPortalContent')
    directivesform.widget(fitxersPerPublicar=MultiFileFieldWidget)
    fitxersPerPublicar = schema.List(title=_(u"Published files"),
                                     value_type=NamedFile(),
                                     required=False,)


class View(grok.View):
    grok.context(IDocument)
    grok.template('document_view')

    def isAnonymous(self):
        from plone import api
        if api.user.is_anonymous():
            return True
        else:
            return False
