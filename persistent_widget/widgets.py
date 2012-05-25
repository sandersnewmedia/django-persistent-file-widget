from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from persistent_widget.utils import (get_media_relative_path, get_media_url,
                                     make_tmp_media_file)


import os
import mimetypes


class PersistentFileWidget(AdminFileWidget):
    """
    A django form file widget that persists between erroneous form submissions.
    """

    template_name = 'persistent_widget/persistent_file_widget.html'

    def __init__(self, *args, **kwargs):
        self.exists = False
        self._upload = None
        super(PersistentFileWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        output = []
        if value:
            try:
                if not self._upload is None:
                    upload = self._upload
                if not hasattr(value, 'url'):
                    # create a temporary file to contain the in-memory-upload
                    upload = value = make_tmp_media_file(value)
                    self._upload = upload
                else:
                    upload = value
                data = self.get_context_data(name=name, value=value,
                                             upload=upload, exists=self.exists)
                output.append(render_to_string(self.template_name, data))
            except IOError:
                pass
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

    def get_context_data(self, **data):
        if self.exists:
            upload = data['upload']
            data['existing_path'] = get_media_relative_path(upload.name)
        return data

    def value_from_datadict(self, data, files, name):
        self.exists = False
        if not files is None and name in files:
            existing_name = '%s-persistent' % name
            existing = data.get(existing_name)
            if existing:
                existing = existing.replace('..', '')
                path = os.path.join(settings.MEDIA_ROOT, existing)
                with open(path, 'r+b') as file:
                    contents = file.read()
                    size = file.tell()
                uploaded_file = InMemoryUploadedFile(
                    file = ContentFile(contents),
                    field_name = name,
                    name = existing,
                    content_type = mimetypes.guess_type(path)[0],
                    size = size,
                    charset = mimetypes.guess_type(path)[1]
                )
                files[name] = uploaded_file
                self.exists = True
        return super(PersistentFileWidget, self).value_from_datadict(data, files, name)


class PersistentImageWidget(PersistentFileWidget):
    """
    A django form file widget that persists between erroneous form submissions
    and displays a thumbnail of images if sorl is installed.
    """
    def get_context_data(self, **data):
        data = super(PersistentImageWidget, self).get_context_data(**data)
        try:
            from sorl.thumbnail import get_thumbnail
            upload = data['upload']
            thumb = get_thumbnail(upload, '100x100', crop='center',
                                  quality=99)
            thumb_url = (get_media_url(thumb.name)
                         if thumb.url.startswith('http:')
                         or thumb.url.startswith('https:')
                         else get_media_url(thumb.url))
            image_url = get_media_url(upload.file.name)
            data.update({ 'image_url': image_url, 'thumb_url': thumb_url })
        except ImportError:
            pass
        return data

