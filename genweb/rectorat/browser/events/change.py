# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from time import strftime


def sessio_changed(session, event):
    """ If rectorat.session change WF to convoque, sends email and
        shows the info in the template
    """
    # si passem estat a convocat cal enviar mail de convocatoria...
    try:
        # Quan crees element també executa aquesta acció, i ID no existeix
        # Fiquem try per fer el bypass
        if event.transition.id == 'convoquing':
            lang = getToolByName(session, 'portal_languages').getPreferredLanguage()

            now = strftime("%d/%m/%Y %H:%M:%S")
            sessiontitle = session.Title()
            place = session.llocConvocatoria
            sessiondate = session.dataSessio.strftime("%d/%m/%Y")
            starthour = session.horaInici.strftime("%H:%M:%S")
            endHour = session.horaFi.strftime("%H:%M:%S")
            organ_path = '/'.join(session.absolute_url_path().split('/')[:-1])
            organ = api.content.get(path=organ_path)

            sender = organ.fromMail
            recipient = organ.adrecaLlista.split(',')

            if lang == 'ca':
                session.notificationDate = now
                subjectMail = "Convocada ordre del dia: " + organ.title
                bodyMail = str(sessiontitle) + ' [' + str(place) + ' ' + str(sessiondate) + '] (' + str(starthour) + '-' + str(endHour) +')'

            if lang == 'es':
                session.notificationDate = now
                subjectMail = "Convocada orden del dia: " + organ.title
                bodyMail = str(sessiontitle) + ' [' + str(place) + ' ' + str(sessiondate) + '] (' + str(starthour) + '-' + str(endHour) +')'

            if lang == 'en':
                now = strftime("%Y-%m-%d %H:%M:%S")
                session.notificationDate = now

                sessiondate = session.dataSessio.strftime("%Y-%m-%d")
                subjectMail = "Convened agenda: " + organ.title
                bodyMail = str(sessiontitle) + ' [' + str(place) + ' ' + str(sessiondate) + '] (' + str(starthour) + '-' + str(endHour) +')'

            api.portal.send_email(recipient=recipient,
                                  sender=sender,
                                  subject=subjectMail,
                                  body=bodyMail,
                                  )
        else:
            # If WF state is not convoquing, do nothing
            pass

    except:
        # No estem canviant d'estat, estem creant l'objecte, passem...
        pass
