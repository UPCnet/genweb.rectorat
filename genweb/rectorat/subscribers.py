from five import grok
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent

from genweb.rectorat.utils import get_settings_property
from genweb.rectorat.content.organgovern import IOrgangovern
from genweb.rectorat.content.sessio import ISessio
from genweb.rectorat.content.document import IDocument
from genweb.rectorat.indicators.updating import (
    update_indicators,
    update_indicators_if_state)


@grok.subscribe(IOrgangovern, IObjectRemovedEvent)
def update_indicators_on_organ_deletion(obj, event):
    update_indicators_if_state(
        obj, ('intranet', 'published'),
        service=get_settings_property('service_id'), indicator='organ-n')


@grok.subscribe(IOrgangovern, IActionSucceededEvent)
def update_indicators_on_organ_review_state_change(obj, event):
    update_indicators(
        obj, service=get_settings_property('service_id'), indicator='organ-n')


@grok.subscribe(ISessio, IObjectRemovedEvent)
def update_indicators_on_sessio_deletion(obj, event):
    update_indicators_if_state(
        obj, ('convocat',),
        service=get_settings_property('service_id'), indicator='sessio-n')


@grok.subscribe(ISessio, IActionSucceededEvent)
def update_indicators_on_sessio_review_state_change(obj, event):
    update_indicators(
        obj, service=get_settings_property('service_id'), indicator='sessio-n')


@grok.subscribe(IDocument, IObjectRemovedEvent)
def update_indicators_on_acord_deletion(obj, event):
    update_indicators_if_state(
        obj, ('intranet', 'published'),
        service=get_settings_property('service_id'), indicator='acord-n')


@grok.subscribe(IDocument, IActionSucceededEvent)
def update_indicators_on_acord_review_state_change(obj, event):
    update_indicators(
        obj, service=get_settings_property('service_id'), indicator='acord-n')
