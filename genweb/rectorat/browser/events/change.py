# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from time import strftime
from zope.annotation.interfaces import IAnnotations
from datetime import datetime
from genweb.rectorat import _


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

            sessiondate = session.dataSessio.strftime("%d/%m/%Y")
            starthour = session.horaInici.strftime("%H:%M")
            endHour = session.horaFi.strftime("%H:%M")
            organ_path = '/'.join(session.absolute_url_path().split('/')[:-1])
            organ = api.content.get(path=organ_path)
            sessionLink = session.absolute_url()
            senderPerson = str(organ.fromMail)

            if session.llocConvocatoria is None:
                place = ''
            else:
                place = session.llocConvocatoria.encode('utf-8')

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
                moreData = '<br/>' + str(customBody) + '<strong>' + str(sessiontitle) + \
                           '</strong><br/><br/>Lloc: ' + str(place) + "<br/>Data: " + str(sessiondate) + \
                           "<br/>Hora d'inici: " + str(starthour) + \
                           "<br/>Hora de fi: " + str(endHour) + \
                           '<br/><br/><strong> Ordre del dia </strong>' + str(ordenField)
                bodyMail = moreData + str(introData)

            if lang == 'es':
                session.notificationDate = now
                subjectMail = "Convocada orden del día: " + organ.title.encode('utf-8')
                introData = "<br/><hr/><p>Puede consultar toda la documentación de la sesión aquí: <a href=" + \
                            str(sessionLink) + ">" + str(sessiontitle) + "</a></p>"
                moreData = '<br/>' + str(customBody) + '<strong>' + str(sessiontitle) + \
                           '</strong><br/><br/>Lugar: ' + str(place) + "<br/>Fecha: " + str(sessiondate) + \
                           "<br/>Hora de inicio: " + str(starthour) + \
                           "<br/>Hora de finalización: " + str(endHour) + \
                           '<br/><br/><strong> Orden del día </strong>' + str(ordenField)
                bodyMail = moreData + str(introData)

            if lang == 'en':
                now = strftime("%Y-%m-%d %H:%M")
                session.notificationDate = now
                sessiondate = session.dataSessio.strftime("%Y-%m-%d")
                subjectMail = "Convened agenda: " + organ.title.encode('utf-8')
                introData = "<br/><hr/><p>You can view the complete session information here:: <a href=" + \
                            str(sessionLink) + ">" + str(sessiontitle) + "</a></p>"
                moreData = '<br/>' + str(customBody) + '<strong>' + str(sessiontitle) + \
                           '</strong><br/><br/>Place: ' + str(place) + "<br/>Date: " + str(sessiondate) + \
                           "<br/>Start time: " + str(starthour) + \
                           "<br/>End time: " + str(endHour) + \
                           '<br/><br/><strong> Contents </strong>' + str(ordenField)
                bodyMail = moreData + str(introData)

            # Sending Mail!
            try:
                addAnnotation(session, recipientPerson)
                session.MailHost.send(bodyMail,
                                      mto=recipientPerson,
                                      mfrom=senderPerson,
                                      subject=subjectMail,
                                      encode=None,
                                      immediate=False,
                                      charset='utf8',
                                      msg_type='text/html')
                session.plone_utils.addPortalMessage(_("Missatge enviat correctament"), 'info')
            except:
                session.plone_utils.addPortalMessage(_("Missatge no enviat. Comprovi el from i el to del missatge"), 'error')


def addAnnotation(object, recipients):
    """ Add annotation after change state and send mail
    """
    KEY = 'genweb.rectorat.logMail'

    annotations = IAnnotations(object)

    if annotations is not None:

        logData = annotations.get(KEY, None)

        try:
            len(logData)
            # Get data and append values
            data = annotations.get(KEY)
        except:
            # If it's empty, initialize data
            data = []

        dateMail = datetime.now()
        username = api.user.get_current().id

        values = dict(dateMail=dateMail,
                      fromMail="Sessió convocada per: " + str(username),
                      toMail=', '.join(map(str, recipients)))

        data.append(values)
        annotations[KEY] = data
