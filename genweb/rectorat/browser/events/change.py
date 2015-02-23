# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from time import strftime


def sessio_changed(session, event):
    """ If rectorat.session change WF to convoque, sends email and
        shows the info in the template
    """
    # si passem estat a convocat cal enviar mail de convocatoria...

    if event.transition is None:
        # Quan crees element també executa aquesta acció, i ID no existeix
        # Fem el bypass
        pass
    else:
        if event.transition.id == 'convoquing':
            lang = getToolByName(session, 'portal_languages').getPreferredLanguage()
            now = strftime("%d/%m/%Y %H:%M:%S")
            sessiontitle = session.Title()
            place = session.llocConvocatoria
            sessiondate = session.dataSessio.strftime("%d/%m/%Y")
            starthour = session.horaInici.strftime("%H:%M")
            endHour = session.horaFi.strftime("%H:%M")
            organ_path = '/'.join(session.absolute_url_path().split('/')[:-1])
            organ = api.content.get(path=organ_path)
            sessionLink = session.absolute_url()
            senderPerson = organ.fromMail

            if session.ordreSessio is None:
                ordenField = ''
            else:
                ordenField = session.ordreSessio.output.encode('utf-8')

            # If no Body ? Continue? Bypass? ...
            if session.bodyMail is None:
                customBody = ''
            else:
                customBody = session.bodyMail.output.encode('utf-8')

            if session.adrecaLlista is None:
                recipientPerson = organ.adrecaLlista.replace(' ', '').encode('utf-8').split(',')
            else:
                recipientPerson = session.adrecaLlista.replace(' ', '').encode('utf-8').split(',')

            if lang == 'ca':
                session.notificationDate = now
                subjectMail = "Convocada ordre del dia: " + organ.title.encode('utf-8')
                introData = "<br/><hr/><p>Podeu consultar tota la documentació de la sessió aquí: <a href=" + \
                            str(sessionLink) + ">" + str(sessiontitle) + "</a></p>"
                moreData = '</br/>' + str(customBody) + '<h2>' + str(sessiontitle) + \
                           '</h2>Lloc: ' + str(place) + "<br/>Data: " + str(sessiondate) + \
                           "<br/>Hora d'inici: " + str(starthour) + \
                           "<br/>Hora de fi: " + str(endHour) + \
                           '<br/><br/><h2> Ordre del dia </h2>' + str(ordenField)
                bodyMail = moreData + str(introData)

            if lang == 'es':
                session.notificationDate = now
                subjectMail = "Convocada orden del día: " + organ.title.encode('utf-8')
                introData = "<br/><hr/><p>Puede consultar toda la documentación de la sesión aquí: <a href=" + \
                            str(sessionLink) + ">" + str(sessiontitle) + "</a></p>"
                moreData = '</br/>' + str(customBody) + '<h2>' + str(sessiontitle) + \
                           '</h2>Lugar: ' + str(place) + "<br/>Fecha: " + str(sessiondate) + \
                           "<br/>Hora de inicio: " + str(starthour) + \
                           "<br/>Hora de finalización: " + str(endHour) + \
                           '<br/><br/><h2> Orden del día </h2>' + str(ordenField)
                bodyMail = moreData + str(introData)

            if lang == 'en':
                now = strftime("%Y-%m-%d %H:%M")
                session.notificationDate = now
                sessiondate = session.dataSessio.strftime("%Y-%m-%d")
                subjectMail = "Convened agenda: " + organ.title.encode('utf-8')
                introData = "<br/><hr/><p>You can view the complete session information here:: <a href=" + \
                            str(sessionLink) + ">" + str(sessiontitle) + "</a></p>"
                moreData = '</br/>' + str(customBody) + '<h2>' + str(sessiontitle) + \
                           '</h2>Place: ' + str(place) + "<br/>Date: " + str(sessiondate) + \
                           "<br/>Start time: " + str(starthour) + \
                           "<br/>End time: " + str(endHour) + \
                           '<br/><br/><h2> Contents </h2>' + str(ordenField)
                bodyMail = moreData + str(introData)

            # Sending Mail!
            session.MailHost.send(bodyMail,
                                  mto=recipientPerson,
                                  mfrom=senderPerson,
                                  subject=subjectMail,
                                  encode=None,
                                  immediate=False,
                                  charset='utf8',
                                  msg_type='text/html')
