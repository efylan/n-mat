from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^casas/$', 'clasificados.views.main_casas', name='main_casas'),
    url(r'^autos/$', 'clasificados.views.main_autos', name='main_autos'),
#    url(r'^review_casa/(?P<casa_id>\d+)/$', 'ventasnorte.caja.views.review_casa', name='review_casa'),
    url(r'^ver_auto/(?P<auto_id>\d+)/$', 'clasificados.views.ver_auto', name='ver_auto'),
    url(r'^ver_casa/(?P<casa_id>\d+)/$', 'clasificados.views.ver_casa', name='ver_casa'),
)

