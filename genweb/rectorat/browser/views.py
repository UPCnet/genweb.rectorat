# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from upc.genweb.newsletter.browser.newsletter import NewsletterBase
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations

from Acquisition import aq_parent,aq_inner


class ActaPrintView(NewsletterBase):

    __call__ = ViewPageTemplateFile('views/acta_print.pt')

    def organGovernTitle(self):
        # Get organGovern Title used for printing the acta
        return self.aq_parent.aq_parent.aq_parent.Title()


class AddLogMail(NewsletterBase):

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)

        valueSenders = self.request.form['recipients-name']

        print "--------------" + valueSenders

        self.request.response.redirect(self.context.absolute_url())
        # key = 'genweb.rectorat.maillog'

        # annotation = IAnnotations(self.context)
        # subscribed = cache.get(key, None)

        # if not subscribed:
        #     subscribed = self._get_max_subscribed_to_context()
        #     cache[key] = subscribed

        # return "HOLA"
