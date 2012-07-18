from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$', 'ventasnorte.users.views.login', name='login'),
    url(r'^logout/$', 'ventasnorte.users.views.logout', name='logout'),
    url(r'^panel/$', 'ventasnorte.users.views.panel', name='user_panel'),
    url(r'^password_change/$', 'ventasnorte.users.views.password_change', name='password_change'),
    url(r'^mis_clasificados/$', 'ventasnorte.users.views.mis_clasificados', name='mis_clasificados'),
    url(r'^mis_favoritos/$', 'ventasnorte.users.views.mis_favoritos', name='mis_favoritos'),

    url(r'^mi_casa/(?P<casa_id>\d+)/$', 'users.views.ver_micasa', name='ver_micasa'),
    url(r'^mi_auto/(?P<auto_id>\d+)/$', 'users.views.ver_miauto', name='ver_miauto'),
    url(r'^reactivar_casa/(?P<casa_id>\d+)/$', 'users.views.reactivar_casa', name='reac_casa'),
    url(r'^reactivar_auto/(?P<auto_id>\d+)/$', 'users.views.reactivar_auto', name='reac_auto'),

    url(r'^crear_casa/$', 'users.views.crear_casa', name='crear_casa_user'),
    url(r'^crear_auto/$', 'users.views.crear_auto', name='crear_auto_user'),

    url(r'^editar_casa/(?P<casa_id>\d+)/$', 'users.views.editar_casa', name='editar_casa_user'),

    url(r'^review_casa/(?P<casa_id>\d+)/$', 'users.views.review_casa', name='review_casa'),
    url(r'^review_auto/(?P<auto_id>\d+)/$', 'users.views.review_auto', name='review_auto'),

    url(r'^venta_casa/(?P<casa_id>\d+)/$', 'users.views.venta_casa', name='venta_casa'),
    url(r'^venta_auto/(?P<auto_id>\d+)/$', 'users.views.venta_auto', name='venta_auto'),
    url(r'^agregar_fotos_casa/(?P<casa_id>\d+)/$', 'users.views.agregar_fotos_casa', name='fotos_casa'),
    url(r'^eliminar_foto_casa/(?P<foto_id>\d+)/$', 'users.views.eliminar_foto_casa', name='rmfotos_casa'),
    url(r'^prin_foto_casa/(?P<foto_id>\d+)/$', 'users.views.foto_prin_casa', name='prfotos_casa'),

)

