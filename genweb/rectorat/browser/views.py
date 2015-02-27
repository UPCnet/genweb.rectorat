# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from upc.genweb.newsletter.browser.newsletter import NewsletterBase
from datetime import datetime


class ActaPrintView(NewsletterBase):

    __call__ = ViewPageTemplateFile('views/acta_print.pt')

    def currentDate(self):
        #import ipdb;ipdb.set_trace()
        #date = api.portal.get_localized_time(datetime.today())
        date = datetime.today().strftime("%d de %b de %Y")
        return date
