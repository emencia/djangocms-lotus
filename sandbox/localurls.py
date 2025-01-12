from django.urls import include, path

from sandbox.urls import urlpatterns


urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
] + urlpatterns
