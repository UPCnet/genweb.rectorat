# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from plone.directives import form
from plone.app.textfield import RichText


from genweb.rectorat import _


class IOrgangovern(form.Schema):
    """ Tipus Sessio: Per a cada Òrgan de Govern es podran crear
        totes les sessions que es considerin oportunes
    """

    descripcioOrgan = RichText(
        title=_(u"Descripció de l'Òrgan de Govern"),
        description=_(u"Descripció de l'Òrgan de Govern"),
        required=False,
    )

    membresOrgan = schema.Text(
        title=_(u"Membres de l'Òrgan de Govern"),
        description=_(u"Membres de l'Òrgan de Govern"),
        required=False,
    )

    adrecaLlista = schema.TextLine(
        title=_(u"Adreça de la llista de distribució"),
        description=_(u"Adreça de la llista de distribució"),
        required=False,
    )

    form.omitted('description')
    description = schema.Bytes()


class View(grok.View):
    grok.context(IOrgangovern)
