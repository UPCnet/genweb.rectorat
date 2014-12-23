# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from time import strftime

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



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
            starthour = session.horaInici.strftime("%H:%M")
            endHour = session.horaFi.strftime("%H:%M")
            organ_path = '/'.join(session.absolute_url_path().split('/')[:-1])
            organ = api.content.get(path=organ_path)

            senderPerson = organ.fromMail
            recipientPerson = organ.adrecaLlista.replace(' ','').encode('utf-8').split(',')
            
            if lang == 'ca':
                session.notificationDate = now
                subjectMail = "Convocada ordre del dia: " + organ.title
                bodyMail = '<h1>' + str(sessiontitle) + '</h1><br/>Lloc: ' + str(place) + "<br/>Hora d'inici: " + str(sessiondate) + '<br/>Hora de fi: ' + str(starthour) + '-' + str(endHour) + '<br/></br/>'
                
            if lang == 'es':
                session.notificationDate = now
                subjectMail = "Convocada orden del dia: " + organ.title
                bodyMail = '<h1>' + str(sessiontitle) + '</h1><br/>Lloc: ' + str(place) + "<br/>Hora d'inici: " + str(sessiondate) + '<br/>Hora de fi: ' + str(starthour) + '-' + str(endHour) + '<br/></br/>'
                
            if lang == 'en':
                now = strftime("%Y-%m-%d %H:%M")
                session.notificationDate = now
                sessiondate = session.dataSessio.strftime("%Y-%m-%d")
                subjectMail = "Convened agenda: " + organ.title
                bodyMail = '<h1>' + str(sessiontitle) + '</h1><br/>Lloc: ' + str(place) + "<br/>Hora d'inici: " + str(sessiondate) + '<br/>Hora de fi: ' + str(starthour) + '-' + str(endHour) + '<br/></br/>'  

            session.MailHost.send(bodyMail,
                    mto=recipientPerson,
                    mfrom=senderPerson,
                    subject=subjectMail,
                    encode=None,
                    immediate=False,
                    charset='utf8',
                    msg_type='text/html')

        else:
            # If WF state is not convoquing, do nothing
            pass

    except:
        # No estem canviant d'estat, estem creant l'objecte, passem...
        pass


