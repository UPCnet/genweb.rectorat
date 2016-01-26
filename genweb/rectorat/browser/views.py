# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from upc.genweb.newsletter.browser.newsletter import NewsletterBase
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from plone import api
from time import strftime
from genweb.rectorat import _


def sessio_sendMail(session, recipients, body):
    """ Si enviem mail des de la sessio.
        Mateix codi que /browser/events/change.py
    """
    lang = getToolByName(session, 'portal_languages').getPreferredLanguage()
    now = strftime("%d/%m/%Y %H:%M:%S")
    sessiontitle = session.Title()

    sessiondate = session.dataSessio.strftime("%d/%m/%Y")
    starthour = session.horaInici.strftime("%H:%M")
    endHour = session.horaFi.strftime("%H:%M")
    sessionLink = session.absolute_url()
    organ_path = '/'.join(session.absolute_url_path().split('/')[:-1])
    organ = api.content.get(path=organ_path)

    if session.llocConvocatoria is None:
        place = ''
    else:
        place = session.llocConvocatoria.encode('utf-8')

    if session.ordreSessio is None:
        ordenField = ''
    else:
        ordenField = session.ordreSessio.output.encode('utf-8')

    # Fixed from modal values
    senderPerson = str(organ.fromMail)
    customBody = body + '<br/><br/>'
    recipientPerson = recipients

    if lang == 'ca':
        session.notificationDate = now
        subjectMail = "Missatge de la sessió: " + str(sessiontitle) + ' - ' + sessiondate
        introData = "<br/><hr/><p>Podeu consultar tota la documentació de la sessió aquí: <a href=" + \
                    str(sessionLink) + ">" + str(sessiontitle) + "</a></p>"
        moreData = '<br/>' + str(customBody) + '<strong>' + str(sessiontitle) + \
                   '</strong><br/><br/>Lloc: ' + str(place) + "<br/>Data: " + str(sessiondate) + \
                   "<br/>Hora d'inici: " + str(starthour) + \
                   "<br/>Hora de fi: " + str(endHour) + \
                   '<br/><br/><strong>Ordre del dia </strong>' + str(ordenField)
        bodyMail = moreData + str(introData)

    if lang == 'es':
        session.notificationDate = now
        subjectMail = "Mensaje de la sesión: " + str(sessiontitle) + ' - ' + sessiondate
        introData = "<br/><hr/><p>Puede consultar toda la documentación de la sesión aquí: <a href=" + \
                    str(sessionLink) + ">" + str(sessiontitle) + "</a></p>"
        moreData = '<br/>' + str(customBody) + '<strong>' + str(sessiontitle) + \
                   '</strong><br/><br/>Lugar: ' + str(place) + "<br/>Fecha: " + str(sessiondate) + \
                   "<br/>Hora de inicio: " + str(starthour) + \
                   "<br/>Hora de finalización: " + str(endHour) + \
                   '<br/><br/><strong>Orden del día </strong>' + str(ordenField)
        bodyMail = moreData + str(introData)

    if lang == 'en':
        now = strftime("%Y-%m-%d %H:%M")
        session.notificationDate = now
        sessiondate = session.dataSessio.strftime("%Y-%m-%d")
        subjectMail = "Session message: " + str(sessiontitle) + ' - ' + sessiondate
        introData = "<br/><hr/><p>You can view the complete session information here:: <a href=" + \
                    str(sessionLink) + ">" + str(sessiontitle) + "</a></p>"
        moreData = '<br/>' + str(customBody) + '<strong>' + str(sessiontitle) + \
                   '</strong><br/><br/>Place: ' + str(place) + "<br/>Date: " + str(sessiondate) + \
                   "<br/>Start time: " + str(starthour) + \
                   "<br/>End time: " + str(endHour) + \
                   '<br/><br/><strong>Contents </strong>' + str(ordenField)
        bodyMail = moreData + str(introData)

    # Sending Mail!
    try:
        session.MailHost.send(bodyMail,
                              mto=recipientPerson,
                              mfrom=senderPerson,
                              subject=subjectMail,
                              encode=None,
                              immediate=False,
                              charset='utf8',
                              msg_type='text/html')
        session.plone_utils.addPortalMessage(
            _("Missatge enviat correctament"), 'info')
    except:
        session.plone_utils.addPortalMessage(
            _("Missatge no enviat. Comprovi els destinataris del missatge"), 'error')


class ActaPrintView(NewsletterBase):

    __call__ = ViewPageTemplateFile('views/acta_print.pt')

    def organGovernTitle(self):
        """ Get organGovern Title used for printing the acta
        """
        return self.aq_parent.aq_parent.aq_parent.Title()


class AddLogMail(BrowserView):

    def __call__(self):
        """ Adding send mail information to context in annotation format
        """
        KEY = 'genweb.rectorat.logMail'
        annotations = IAnnotations(self.context)
        send = True
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

            anon = api.user.is_anonymous()
            if not anon:
                username = api.user.get_current().id
            else:
                username = ''

            body = ''  # Fiquem el body buit per si de cas...
            try:
                # If someone access directly to this view... do nothing
                toMail = self.request.form['recipients-name']
                body = self.request.form['message-text']
            except:
                return

            if send is True:
                values = dict(dateMail=dateMail,
                              fromMail=_("Missatge enviat per: ") + username,
                              toMail=toMail)

                data.append(values)
                annotations[KEY] = data

                sessio_sendMail(self.context, toMail, body)  # Enviem mail
        # session, sender, recipients, body

        self.request.response.redirect(self.context.absolute_url())


# Notificar canvi -> Enviar missatge
