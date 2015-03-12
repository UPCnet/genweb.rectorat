# -*- coding: utf-8 -*-
from genweb.rectorat.content.document import IDocument
from collective.dexteritytextindexer.converters import DefaultDexterityTextIndexFieldConverter
from collective.dexteritytextindexer.interfaces import IDexterityTextIndexFieldConverter
from plone.dexterity.interfaces import IDexterityContent
from z3c.form.interfaces import IWidget
from zope.component import adapts
from zope.interface import implements
from zope.schema.interfaces import IField
from Products.CMFCore.utils import getToolByName

from plone.formwidget.multifile.widget import MultiFileWidget, MultiFileFieldWidget
from plone.formwidget.multifile.interfaces import IMultiFileWidget


class SearchableText(DefaultDexterityTextIndexFieldConverter):
    implements(IDexterityTextIndexFieldConverter)
    adapts(IDexterityContent, IField, IWidget )

    def __init__(self, context, field, widget):
        """Initialize field converter"""
        self.context = context
        self.field = field
        self.widget = widget

    def convert(self):
        # implement your custom converter
        # which returns a string at the end
        searchableText =[]
        if self.widget.id == 'PublishedFiles':
            for obj in self.widget.value:
            	# import ipdb;ipdb.set_trace()

                name = obj.filename.encode('utf-8')
                transforms = getToolByName(self.context, 'portal_transforms')
                # if isinstance(html, unicode):
                #     html = html.encode('utf-8')
                stream = transforms.convertTo('text/plain', obj.data, mimetype='text/html')
                searchableText.append(name)
                searchableText.append(stream.getData().strip())
        else:
            html = self.widget.render().strip()
            # self.widget.value[0].filename

            transforms = getToolByName(self.context, 'portal_transforms')
            if isinstance(html, unicode):
                html = html.encode('utf-8')
            stream = transforms.convertTo('text/plain', html, mimetype='text/html')
            searchableText = stream.getData().strip()
        return str(searchableText)
