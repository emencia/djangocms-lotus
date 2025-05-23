"""
Django settings for demonstration

Intended to be used with ``make run``.
"""
from sandbox.settings.base import *  # noqa: F403

DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": VAR_PATH / "db" / "db.sqlite3",  # noqa: F405
    }
}


"""
django-debug-toolbar part

This is only applied if package has been installed.
"""
try:
    import debug_toolbar
except ImportError:
    pass
else:
    ROOT_URLCONF = "sandbox.localurls"

    INTERNAL_IPS = ["192.168.0.115"]

    DEBUG_TOOLBAR_PANELS = [
        # "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        # "debug_toolbar.panels.signals.SignalsPanel",
        # "debug_toolbar.panels.redirects.RedirectsPanel",
        # "debug_toolbar.panels.profiling.ProfilingPanel",
    ]

    MIDDLEWARE[0:0] = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INSTALLED_APPS.append("debug_toolbar")


# Import local settings if any
try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass
