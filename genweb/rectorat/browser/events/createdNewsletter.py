# -*- coding: utf-8 -*-
from plone import api
from genweb.rectorat import _


def createdNewsletter(value, event):
    """ La primera vegada que es crea un Butlletí li copia
        l'estructura del template per defecte
    """

    portal = api.portal.get()
    try:
        # /ca/plantilles-butlletins/plantilla/template-base/
        template = portal['ca']['plantilles-butlletins']['plantilla']['template-base']['row']
        api.content.copy(source=template, target=value)
    except:
        value.plone_utils.addPortalMessage(_("No s'ha pogut copiar la plantilla per defecte. El fitxer amb les dades, no existeix: /ca/plantilles-butlletins/plantilla/template-base"), 'error')
