# -*- coding: utf-8 -*-
from plone import api
import re
import datetime
from five import grok
from cgi import escape
from Acquisition import aq_inner
import zope.component
from datetime import datetime
from zope.schema import TextLine
from z3c.form import field, button
from plone.directives import form
from Products.CMFPlone.utils import safe_unicode
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from genweb.rectorat.interfaces import IGenwebRectoratLayer
from plone.app.textfield import RichText
from zope.interface import Interface
from genweb.rectorat import _
from genweb.rectorat.content.sessio import ISessio
from zope.annotation.interfaces import IAnnotations
from genweb.rectorat.browser.views import sessio_sendMail

grok.templatedir("send_templates")

MESSAGE_TEMPLATE = u"""\
Ha recibido este correo porque %(name)s (%(mail)s) ha rellenado \
el formulario de contacto en \

  %(path)s

ASUNTO:

  %(asunto)s

MENSAJE:

  %(observaciones)s

--
Fecha consulta: %(date)s
"""


class IMessage(form.Schema):
    """ Define the fields of this form
    """

    recipients = TextLine(
        title=_("Recipients"),
        description=_("Mail address separated by commas."),
        required=False)

    message = RichText(
        title=_('Message'),
        description=_("This content will be used as message content"),
        required=False)


class Message(form.SchemaForm):
    grok.name('send_message')
    grok.context(ISessio)
    grok.template("message_view")
    grok.require('zope2.View')
    grok.layer(IGenwebRectoratLayer)

    ignoreContext = True

    schema = IMessage

    # fields = field.Fields(IMessage)

    # This trick hides the editable border and tabs in Plone
    def update(self):
        self.request.set('disable_border', True)
        super(Message, self).update()

    def updateWidgets(self):
        super(Message, self).updateWidgets()
        self.widgets["recipients"].value = self.context.adrecaLlista

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        message = _(u"Operation Cancelled.")
        IStatusMessage(self.request).addStatusMessage(message, type="warning")
        return self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u"Send"))
    def action_send(self, action):
        """ Send the email to the configured mail address 
            in properties and redirect to the
            front page, showing a status message to say
            the message was received. """

        emptyfields = []

        formData, errors = self.extractData()
        lang = self.context.language

        if formData['recipients'] is None or formData['message'] is None:

            if formData['recipients'] is None:
                if lang == 'ca':
                    emptyfields.append("Destinataris")
                elif lang == 'es':
                    emptyfields.append("Destinatarios")
                else:
                    emptyfields.append("Recipients")

            if formData['message'] is None:
                if lang == 'ca':
                    emptyfields.append("Missatge")
                elif lang == 'es':
                    emptyfields.append("Mensaje")
                else:
                    emptyfields.append("Message")

            empty = ', '.join(emptyfields) + '.'
            if lang == 'ca':
                message = "Falten camps obligatorios: "
            if lang == 'es':
                message = "Faltan campos obligatorios: "
            if lang == 'en':
                message = "Required fields missing: "
            IStatusMessage(self.request).addStatusMessage(message + empty, type="error")
            return

        """ Adding send mail information to context in annotation format
        """
        KEY = 'genweb.rectorat.logMail'
        annotations = IAnnotations(self.context)

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

            toMail = str(formData['recipients'])
            body = str(formData['message'].output)

            values = dict(dateMail=dateMail,
                          fromMail=_("Missatge enviat per: ") + username,
                          toMail=toMail)

            data.append(values)
            annotations[KEY] = data

            sessio_sendMail(self.context, toMail, body)  # Enviem mail

        return self.request.response.redirect(self.context.absolute_url())
