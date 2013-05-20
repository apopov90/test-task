from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'test1.views.Index', name="Index"),
    url(r'^load-model/$', 'test1.views.LoadModel', name="loadmodel"),
    url(r'^update-model/$', 'test1.views.UpdateModel', name="updateobject"),
    url(r'^add-to-model/$', 'test1.views.AddNew', name="add_to_model"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        }),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
        }),
)
