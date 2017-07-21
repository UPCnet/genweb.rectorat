# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from plone import api
import transaction
import logging

filename = 'moveHistoric.log'  # local
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=filename,
                    level=logging.DEBUG)


def pp(message, item, f="None"):
    """Function to show messages in file and screen """
    if f is "None":
        f = open(filename, 'a')
    if item is not None:
        print " ## " + str(message) + " @@ " + str(item)
        f.write(" ## " + str(message) + " @@ " + str(item) + "\n")
    if message is "Close":
        f.close()


class moveHistoric(BrowserView):

    def __call__(self):
        """ Used in migrate Organs from v1.0 to v2.0 """
        date = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        pp('-------------------------------------------------------', '')
        pp("START Move Historic folders", date)
        pp('-------------------------------------------------------', '')
        portal_catalog = getToolByName(self, 'portal_catalog')

        historic_items = portal_catalog.searchResults(
            portal_type='genweb.rectorat.historicfolder'
        )

        for histfolder in historic_items:
            tomove = histfolder.getObject().items()
            for objc in tomove:
                origen = objc[1]
                destino = objc[1].aq_parent.aq_parent
                try:
                    api.content.move(source=origen, target=destino)
                    pp('OK. Moved', str(origen.absolute_url_path()) + ' > ' + str(destino.absolute_url_path()))
                except:
                    pp('ERROR. MOVING...', str(origen.absolute_url_path()) + ' > ' + str(origen.portal_type))
        transaction.commit()

        date = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        pp('-------------------------------------------------------', '')
        pp("END. Check ERROR. MOVING string", date)
        pp('-------------------------------------------------------', '')
        pp("Close", None)

        result = []
        with open(filename) as f:
            line = f.read()
            result.append(line)

        return result[0]
