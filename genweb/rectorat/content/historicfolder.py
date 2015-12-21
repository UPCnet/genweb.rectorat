# -*- coding: utf-8 -*-
from five import grok
from plone.directives import form


class IHistoricfolder(form.Schema):
    """ Tipus Històric Folder: Permet crear carpetes
        dintre dels Organs de Govern per fer un historic
        de sessions
    """


class View(grok.View):
    grok.context(IHistoricfolder)
    grok.template('historicfolder_view')
