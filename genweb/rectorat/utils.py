# -*- coding: utf-8 -*-

from zope.component import getUtility
from plone import api
from plone.registry.interfaces import IRegistry

from genweb.rectorat.controlpanel import IRectoratSettings


def isReader(self):
    """ Returns true if user is Reader or Manager """
    try:
        if api.user.is_anonymous():
            return False
        else:
            username = api.user.get_current().getProperty('id')
            roles = api.user.get_roles(username=username, obj=self.context)
            if 'Reader' in roles or 'Manager' in roles:
                return True
            else:
                return False
    except:
        return False


def isEditor(self):
    """ Return true if user is Editor or Manager """
    try:
        username = api.user.get_current().getProperty('id')
        roles = api.user.get_roles(username=username, obj=self.context)
        if 'Editor' in roles or 'Manager' in roles:
            return True
        else:
            return False
    except:
        return False


def get_settings_property(property_id):
    settings = getUtility(IRegistry).forInterface(IRectoratSettings)
    return getattr(settings, property_id, None)
