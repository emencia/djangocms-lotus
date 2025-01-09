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

Settings
********

.. automodule:: djangocms_lotus.settings
   :members:
