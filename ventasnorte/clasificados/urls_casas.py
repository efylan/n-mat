from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'clasificados.views.main_casas', name='main_casas'),
    url(r'^detalle_casa/(?P<casa_id>\d+)/$', 'clasificados.views.ver_casa', name='ver_casa'),
    url(r'^fav_casa/(?P<casa_id>\d+)/$', 'clasificados.views.fav_casa', name='fav_casa'),
    url(r'^rmfav_casa/(?P<casa_id>\d+)/$', 'clasificados.views.rmfav_casa', name='rmfav_casa'),
    url(r'^desactivar_casa/(?P<casa_id>\d+)/$', 'clasificados.views.apagar_casa', name='apagar_casa'),
    url(r'^categorias/$', 'clasificados.views.categorias_casas', name='categorias_casas'),
    url(r'^categorias/(?P<categoria_slug>[-\w]+)/$', 'clasificados.views.disponibilidad_casas', name='disponibilidad_casas'),
    url(r'^categorias/(?P<categoria_slug>[-\w]+)/(?P<dispo_slug>[-\w]+)/$', 'clasificados.views.catdis_casas', name='catdis_casas'),
    url(r'^busqueda_simple/$', 'clasificados.views.simple_search_casas', name='ssearch_casas'),
#    url(r'^modelos/(?P<modelo_slug>[-\w]+)/$', 'clasificados.views.series_autos', name='series_autos'),
    url(r'^album_casa/(?P<casa_id>\d+)/$', 'clasificados.views.album_casa', name='album_casa'),
    url(r'^busqueda_texto/$', 'clasificados.views.text_search_casa', name='tsearch_casas'),
)

