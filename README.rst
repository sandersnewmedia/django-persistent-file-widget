=============================
django-persistent-file-widget
=============================

A django form file widget that persists between erroneous form submissions!

Usage
-----

1. Run ``pip install django-persistent-file-widget`` or place ``persistent_widget`` on your Python path.

2. Add ``persistent_widget`` to your list of ``INSTALLED_APPS``.

3. There are two widgets available, ``persistent_widget.widgets.PersistentFileWidget`` and ``persistent_widget.widgets.PersistentImageWidget``.  The latter will display a thumbnail if ``sorl.thumbnail`` is installed.

