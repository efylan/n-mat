from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'clasificados.views.main_autos', name='main_autos'),
    url(r'^detalle_auto/(?P<auto_id>\d+)/$', 'clasificados.views.ver_auto', name='ver_auto'),
    url(r'^fav_auto/(?P<auto_id>\d+)/$', 'clasificados.views.fav_auto', name='fav_auto'),
    url(r'^rmfav_auto/(?P<auto_id>\d+)/$', 'clasificados.views.rmfav_auto', name='rmfav_auto'),
    url(r'^desactivar_auto/(?P<auto_id>\d+)/$', 'clasificados.views.apagar_auto', name='apagar_auto'),
    url(r'^marcas/$', 'clasificados.views.marcas_autos', name='marcas_autos'),
    url(r'^marcas/(?P<marca_slug>[-\w]+)/$', 'clasificados.views.modelos_autos', name='modelos_autos'),
    url(r'^modelos/(?P<modelo_slug>[-\w]+)/$', 'clasificados.views.series_autos', name='series_autos'),
    url(r'^busqueda_simple/$', 'clasificados.views.simple_search_autos', name='ssearch_autos'),
    url(r'^combo_dependiente/$', 'clasificados.views.combo_dependiente_autos', name='combo_mm'),
    url(r'^album_auto/(?P<auto_id>\d+)/$', 'clasificados.views.album_auto', name='album_auto'),
    url(r'^busqueda_texto/$', 'clasificados.views.text_search_auto', name='tsearch_autos'),
)

