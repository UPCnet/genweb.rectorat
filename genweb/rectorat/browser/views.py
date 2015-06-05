# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from upc.genweb.newsletter.browser.newsletter import NewsletterBase
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from datetime import datetime


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

        if annotations is not None:

            logData = annotations.get(KEY, None)

            if logData is (None or ''):
                # If it's emppty, initialize data
                data = []
            else:
                # Else, get data and append values
                data = annotations.get(KEY)

            dateMail = datetime.now()
            fromMail = 'TEST_USER'  # TODO: Obtain username
            try:
                # If someone access directly to this view... do nothing
                toMail = self.request.form['recipients-name']
            except:
                return

            values = dict(dateMail=dateMail,
                          fromMail=fromMail,
                          toMail=toMail)
            data.append(values)
            annotations[KEY] = data

        self.request.response.redirect(self.context.absolute_url())
