# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from upc.genweb.newsletter.browser.newsletter import NewsletterBase
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from datetime import datetime


class ActaPrintView(NewsletterBase):

    __call__ = ViewPageTemplateFile('views/acta_print.pt')

    def organGovernTitle(self):
        # Get organGovern Title used for printing the acta
        return self.aq_parent.aq_parent.aq_parent.Title()


class AddLogMail(NewsletterBase):

    def __init__(self, context, request):
        """ Adding send mail information to context in annotation format
        """
        super(BrowserView, self).__init__(context, request)

        valueSenders = self.request.form['recipients-name']

        KEY = 'genweb.rectorat.maillog'

        annotations = IAnnotations(self.context)
        if annotations is not None:

            logData = annotations.get(KEY, '')
            annotations[KEY] = str(valueSenders) + str(logData)

        self.request.response.redirect(self.context.absolute_url())
