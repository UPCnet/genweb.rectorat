# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
import transaction
import logging


filename = 'blanks.log'  # local
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=filename,
                    level=logging.DEBUG)


def pp(message, item, f="None"):
    """Function to show messages in file and screen """
    if f is "None":
        f = open(filename, 'a')
    if item is not None:
        print "## " + str(message) + " @@ " + str(item)
        f.write("## " + str(message) + " @@ " + str(item) + "\n")
    if message is "Close":
        f.close()


class findblanks(BrowserView):

    def __call__(self):
        """ Migrate Organs from v1.0 to v2.0 """
        items = api.content.find(
            type='genweb.organs.document',
            context=api.portal.get(),
        )
        pp('-------------------------------', '')
        pp('Entries with NO proposalPoint', '')
        pp('-------------------------------', '')
        for item in items:
            value = item.getObject()
            if hasattr(value, 'proposalPoint'):
                if value.proposalPoint is None:
                    pp('Added 00', value.absolute_url())
                    value.proposalPoint = '00'
                    transaction.commit()
        pp('-------------------------------', '')
        pp('Entries with - in proposalPoint', '')
        pp('-------------------------------', '')
        for item in items:
            value = item.getObject()
            if hasattr(value, 'proposalPoint'):
                if '-' in value.proposalPoint:
                    value.proposalPoint = value.proposalPoint.replace('-', '')
                    pp('Replaced -', str(value.proposalPoint))
                    transaction.commit()

        pp('-------------------------------', '')
        pp('Entries with . in proposalPoint', '')
        pp('-------------------------------', '')
        for item in items:
            value = item.getObject()
            if hasattr(value, 'proposalPoint'):
                if '.' in value.proposalPoint:
                    if '.' in value.proposalPoint[-1]:
                        value.proposalPoint = value.proposalPoint[:-1]
                        transaction.commit()
                        pp('Removed . from end ', str(value.proposalPoint) + ' > ' + value.absolute_url())
        pp('-------------------------------', '')
        items = api.content.find(
            type='genweb.organs.document',
            context=api.portal.get(),
        )
        pp('-------------------------------', '')
        pp('    FINAL ENTRIES', '')
        pp('-------------------------------', '')
        for item in items:
            value = item.getObject()
            if hasattr(value, 'proposalPoint'):
                try:
                    pp('', str(value.proposalPoint) + ' ')
                except:
                    pp('Codi erroni', str(value.proposalPoint.encode('utf-8')) + ' > ' + str(value.absolute_url()))
                    value.proposalPoint = '0'
                    transaction.commit()
        pp('-------------------------------', '')

        result = []
        with open(filename) as f:
            line = f.read()
            result.append(line)
        return result[0]
