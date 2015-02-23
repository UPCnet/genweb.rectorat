# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.namedfile.field import NamedFile
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.formwidget.multifile import MultiFileFieldWidget
from plone.directives import dexterity
from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.supermodel import model
from z3c.form.interfaces import INPUT_MODE, DISPLAY_MODE, HIDDEN_MODE
from plone import api
from collective import dexteritytextindexer


class IActa(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    membresConvocats = RichText(
        title=_(u"Incoming members list"),
        required=False,
    )

    membresConvidats = RichText(
        title=_(u"Invited members"),
        required=False,
    )

    llistaExcusats = RichText(
        title=_(u"Excused members"),
        required=False,
    )

    llistaNoAssistens = RichText(
        title=_(u"Missing members"),
        required=False,
    )

    dexteritytextindexer.searchable('ordreSessio')
    ordreSessio = RichText(
        title=_(u"Session order"),
        required=False,
    )

    dexteritytextindexer.searchable('actaBody')
    actaBody = RichText(
        title=_(u"Acta Body"),
        required=False,
    )

    dexteritytextindexer.searchable('OriginalFiles')
    form.widget(OriginalFiles=MultiFileFieldWidget)
    OriginalFiles = schema.List(title=_(u"Files"),
                                value_type=NamedFile(),
                                required=False,)


@form.default_value(field=IActa['membresConvidats'])
def membresConvidatsDefaultValue(data):
    # copy membresConvidats from Session (parent object)
    return data.context.membresConvidats


@form.default_value(field=IActa['membresConvocats'])
def membresConvocatsDefaultValue(data):
    # copy membresConvocats from Session (parent object)
    return data.context.membresConvocats


@form.default_value(field=IActa['llistaExcusats'])
def llistaExcusatsDefaultValue(data):
    # copy llistaExcusats from Session (parent object)
    return data.context.llistaExcusats


@form.default_value(field=IActa['ordreSessio'])
def ordreSessioDefaultValue(data):
    # copy ordreSessio from Session (parent object)
    return data.context.ordreSessio


@form.default_value(field=IActa['actaBody'])
def actaBodyDefaultValue(data):
    # copy ordreSessio from Session in Acta
    return data.context.ordreSessio


class View(dexterity.DisplayForm):
    grok.context(IActa)
    grok.template('acta_view')

    def isAuthenticated(self):
        if api.user.is_anonymous():
            return False
        else:
            return True


class Edit(dexterity.EditForm):
    """A standard edit form.
    """
    grok.context(IActa)