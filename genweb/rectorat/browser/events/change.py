# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from time import strftime


def sessio_changed(document, event):
    """ If rectorat.document change WF to convoque, sends email and
        shows the info in the template
    """
    # si passem estat a convocat cal enviar mail de convocatoria...
    try:
        # Quan crees element també executa aquesta acció, i ID no existeix
        # Fiquem try per fer el bypass
        if event.transition.id == 'convoquing':
            lang = getToolByName(document, 'portal_languages').getPreferredLanguage()

            if lang == 'ca':
                now = strftime("%d/%m/%Y %H:%M:%S")
                document.notificationDate = now
                subjectMail = "Convocada ordre del dia"
                bodyMail = 'Contingut en Català'

            if lang == 'es':
                now = strftime("%d/%m/%Y %H:%M:%S")
                document.notificationDate = now
                subjectMail = "Convocada orden del dia"
                bodyMail = 'Contenido en castellano'

            if lang == 'en':
                now = strftime("%Y-%m-%d %H:%M:%S")
                document.notificationDate = now
                subjectMail = "Convened agenda"
                bodyMail = 'English content'

            api.portal.send_email(recipient="bob@plone.org",
                                  sender="noreply@plone.org",
                                  subject=subjectMail,
                                  body=bodyMail,
                                  )
        else:
            pass

    except:
        # No estem canviant d'estat, estem creant l'objecte, passem...
        pass
