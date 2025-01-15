.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install djangocms-lotus

For development usage see :ref:`development_install`.

Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "djangocms_lotus",
    )

Then load default application settings in your settings file: ::

    from djangocms_lotus.settings import *

Then mount applications URLs: ::

    urlpatterns = [
        ...
        path("", include("djangocms_lotus.urls")),
    ]

And finally apply database migrations.

Lotus admin layout fix with 'django-admin-style'
------------------------------------------------

Application 'django-admin-style' overrides a lot of things in the Django admin layout
and so breaks custom styles like the ones from Lotus (which fix CKEditor and Category
tree layout).

This package includes a stylesheet that patch these issues but you need to configure
its usage in settings. Put this in your settings after the Lotus settings part: ::

    LOTUS_ADMIN_ALBUM_ASSETS["css"]["all"] = ("css/cmslotus-admin/lotus-admin.css",)
    LOTUS_ADMIN_ARTICLE_ASSETS["css"]["all"] = ("css/cmslotus-admin/lotus-admin.css",)
    LOTUS_ADMIN_CATEGORY_ASSETS["css"]["all"] = ("css/cmslotus-admin/lotus-admin.css",)

Without it this will be the Lotus stylesheet that will be used, you may suffer suffer
of some minor layout issues with CKEditor and Category tree.

.. Note::
    This is probably a temporary thing because Lotus will probably includes this
    stylesheet compatilibity fixes in a further release.

Settings
********

.. automodule:: djangocms_lotus.settings
   :members:
