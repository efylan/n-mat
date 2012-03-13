from django.conf.urls.defaults import patterns, include, url
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ventasnorte.views.index', name='index'),
    url(r'^usuarios/', include('users.urls')),
    url(r'^caja/', include('caja.urls')),
    url(r'^casas/', include('clasificados.urls_casas')),
    url(r'^autos/', include('clasificados.urls_autos')),
    url(r'^lugares/', include('lugares.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views',(r'^media/(?P<path>.*)$', 'static.serve', {'document_root': MEDIA_ROOT}))
