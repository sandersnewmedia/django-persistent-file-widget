
from django.conf import settings
from django.core.files import File

import os

def get_media_url(path, full=False):
    "returns the url relative to MEDIA_URL give a path relative to MEDIA_ROOT"

    if path.startswith('http:') or path.startswith('https:'):
        return path

    path = os.path.abspath(path)

    media_root = os.path.abspath(settings.MEDIA_ROOT)
    if not media_root.endswith('/'):
        media_root = media_root + '/'

    media_url = settings.MEDIA_URL
    if not media_url.endswith('/'):
        media_url = media_url + '/'
    return path.replace(media_root, media_url)


def get_media_relative_path(path):
    "returns the path relative to MEDIA_ROOT that this file lives at"
    media_root = os.path.abspath(settings.MEDIA_ROOT)
    if not media_root.endswith('/'):
        media_root = media_root + '/'
    return path.replace(media_root, '')


class MediaFile(File):

    @property
    def url(self):
        return get_media_url(self.name)

def make_tmp_media_file(fileobj):
    """
    Copies an InMemoryUploadedFile, File, or ContentFile to a file available
    at MEDIA_URL
    """
    i = 0
    dirname = os.path.join(settings.MEDIA_ROOT, 'tmp')
    path = os.path.join(dirname, fileobj.name)
    try:
        # make the parent directories if they don't exist
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass
    fileobj.seek(0)
    contents = fileobj.read()
    with open(path, 'w+b') as f:
        f.write(contents)
    fileobj.seek(0)
    return MediaFile(open(path, 'r+b'), name=get_media_relative_path(path))

