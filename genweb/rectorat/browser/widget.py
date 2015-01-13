from Acquisition import aq_inner
from plone.namedfile.utils import set_headers, stream_data
from Products.Five.browser import BrowserView
from z3c.form.interfaces import IFieldWidget, IDataManager, NO_VALUE
from z3c.form.widget import FieldWidget, Widget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.interface import implements, implementer
from zope.publisher.interfaces import IPublishTraverse, NotFound

from plone.formwidget.multifile.interfaces import IMultiFileWidget
from plone.formwidget.multifile.utils import get_icon_for

from plone import api
from AccessControl import Unauthorized

class Download(BrowserView):
    """Download a file via ++widget++widget_name/@@download/filename"""

    implements(IPublishTraverse)

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.file_index = None
        self.content = None

    def publishTraverse(self, request, name):

        try:
            if self.file_index is None: # ../@@download/file_index
                self.file_index = int(name)
                return self
            elif self.file_index == name:
                return self
        except ValueError:
            # NotFound raised below
            pass

        raise NotFound(self, name, request)

    def __call__(self):

        if self.context.ignoreContext:
            raise NotFound("Cannot get the data file from a widget with no context")

        if self.context.form is not None:
            content = aq_inner(self.context.form.getContent())
        else:
            content = aq_inner(self.context.context)
        field = aq_inner(self.context.field)

        dm = getMultiAdapter((content, field,), IDataManager)
        file_list = dm.get()
        try:
            file_ = file_list[self.file_index]
        except (IndexError, TypeError):
            raise NotFound(self, self.file_index, self.request)

        filename = getattr(file_, 'filename', '')

        set_headers(file_, self.request.response, filename=filename)

        if 'OriginalFiles' in self.context.id:
        # Original Files only visible by validated users...
        # Add permissions to "download file"
            if api.user.is_anonymous():
                # is anon
                raise Unauthorized('You have no permissions to download this file.')
            else:
                # Is a validated user...
                username = api.user.get_current().getProperty('id')
                # get username

                roles = api.user.get_roles(username=username, obj=self.context)
                # And check roles
                if 'Reader' in roles:
                    return stream_data(file_)
                else:
                    raise Unauthorized("You have no permissions to download this file")
        else:
            return stream_data(file_)
