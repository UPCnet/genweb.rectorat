# -*- coding: utf-8 -*-
import re
import datetime
from five import grok
from cgi import escape
from Acquisition import aq_inner
import zope.component
from zope.schema import TextLine, Text
from z3c.form import field, button
from plone.directives import form
from Products.CMFPlone.utils import safe_unicode
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from genweb.rectorat.interfaces import IGenwebRectoratLayer
from plone.app.textfield import RichText
from zope.interface import Interface
from genweb.rectorat import _


grok.context(Interface)
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

check_email = re.compile(r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}").match


def validate_email(value):
    if not check_email(value):
        raise zope.interface.Invalid(_(u"Invalid email address"))
    return True


class IContact(form.Schema):
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


class Contact(form.Form):
    grok.name('send_message')
    grok.context(Interface)
    grok.template("message_view")
    grok.require('zope2.View')
    grok.layer(IGenwebRectoratLayer)

    ignoreContext = True

    fields = field.Fields(IContact)

    # This trick hides the editable border and tabs in Plone
    def update(self):
        self.request.set('disable_border', True)
        super(Contact, self).update()

    @button.buttonAndHandler(_(u"Send"))
    def action_send(self, action):
        """ Send the email to the configured mail address 
            in properties and redirect to the
            front page, showing a status message to say
            the message was received. """

        emptyfields = []

        data, errors = self.extractData()
        lang = self.context.language

        if 'recipients' not in data or 'message' not in data:
            if 'recipients' not in data:
                if lang == 'ca':
                    emptyfields.append("Destinataris")
                if lang == 'es':
                    emptyfields.append("Destinatarios")
                else:
                    emptyfields.append("Recipients")
            if 'message' not in data:
                if lang == 'ca':
                    emptyfields.append("Missatge")
                if lang == 'es':
                    emptyfields.append("Mensaje")
                else:
                    emptyfields.append("Message")

            empty = ', '.join(emptyfields) + '.'
            if lang == 'ca':
                error_message = "Falten camps obligatorio: "
            if lang == 'es':
                error_message = "Faltan campos obligatorios: "
            if lang == 'en':
                error_message = "Required fields missing: "
            IStatusMessage(self.request).addStatusMessage(error_message + empty, type="")
            return

        context = aq_inner(self.context)
        mailhost = getToolByName(context, 'MailHost')
        urltool = getToolByName(context, 'portal_url')
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')

        to_address = portal.getProperty('email_from_address')

        source = "%s <%s>" % (escape(safe_unicode(data['name'])),
                              escape(safe_unicode(data['mail'])))
        subject = escape(safe_unicode(_(u"[Formulario de Contacto] "))) + escape(safe_unicode(data['name']))

        message = MESSAGE_TEMPLATE % dict(name=data['name'],
                                          mail=data['mail'],
                                          path=self.context.absolute_url(),
                                          observaciones=data['message'],
                                          asunto=data['asunto'],
                                          date=datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
                                          )

        mailhost.secureSend(escape(safe_unicode(message)),
                            to_address,
                            source,
                            subject=subject, subtype='plain',
                            charset=email_charset, debug=False,
                            )

        info_message = _(u"Mail sent.")
        IStatusMessage(self.request).addStatusMessage(info_message, type="")

        return self.request.response.redirect(portal.absolute_url())
