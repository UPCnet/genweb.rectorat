# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText

from genweb.rectorat import _
from plone.app.dexterity import PloneMessageFactory as _PMF
from collective import dexteritytextindexer
from plone.app.users.userdataschema import checkEmailAddress


class IHistoricfolder(form.Schema):
    """ Tipus Històric Folder: Permet crear carpetes
        dintre dels Organs de Govern per fer un historic
        de sessions
    """


class View(grok.View):
    grok.context(IHistoricfolder)
    grok.template('historicfolder_view')
