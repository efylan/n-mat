from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^crear_ccasa/$', 'ventasnorte.caja.views.crear_ccasa', name='crear_ccasa'),
    url(r'^crear_cauto/$', 'ventasnorte.caja.views.crear_cauto', name='crear_cauto'),
    url(r'^panel/$', 'ventasnorte.caja.views.panel', name='panel_caja'),
    url(r'^review_casa/(?P<casa_id>\d+)/$', 'ventasnorte.caja.views.review_casa', name='review_casa'),
    url(r'^review_auto/(?P<auto_id>\d+)/$', 'ventasnorte.caja.views.review_auto', name='review_auto'),
    url(r'^agregar_fotos_casa/(?P<casa_id>\d+)/$', 'ventasnorte.caja.views.agregar_fotos_casa', name='fotos_casa'),
    url(r'^agregar_fotos_auto/(?P<auto_id>\d+)/$', 'ventasnorte.caja.views.agregar_fotos_auto', name='fotos_auto'),
    url(r'^eliminar_foto_casa/(?P<foto_id>\d+)/$', 'ventasnorte.caja.views.eliminar_foto_casa', name='rmfotos_casa'),
    url(r'^eliminar_foto_auto/(?P<foto_id>\d+)/$', 'ventasnorte.caja.views.eliminar_foto_auto', name='rmfotos_auto'),
    url(r'^prin_foto_casa/(?P<foto_id>\d+)/$', 'ventasnorte.caja.views.foto_prin_casa', name='prfotos_casa'),
    url(r'^prin_foto_auto/(?P<foto_id>\d+)/$', 'ventasnorte.caja.views.foto_prin_auto', name='prfotos_auto'),


    url(r'^editar_casa/(?P<casa_id>\d+)/$', 'ventasnorte.caja.views.editar_casa', name='editar_casa'),
    url(r'^editar_auto/(?P<auto_id>\d+)/$', 'ventasnorte.caja.views.editar_auto', name='editar_auto'),
    url(r'^registro_usuario/$', 'ventasnorte.caja.views.registrar_usuario', name='registro_usuario'),    
    url(r'^mostrar/$', 'ventasnorte.caja.views.mostrar_usuario', name='mostrar_usuario'),
    url(r'^usuarios/consultar/$', 'ventasnorte.caja.views.usuarios_consultar', name='mostrar_usuario'),
    url(r'^modificaciones/$', 'ventasnorte.caja.views.modificaciones', name='modificaciones'),
    url(r'^modificaciones/id_search/$', 'ventasnorte.caja.views.id_search', name='modif_id_search'),
    url(r'^modificaciones/name_search/$', 'ventasnorte.caja.views.name_search', name='modif_name_search'),
    url(r'^detalle_usuario/(?P<user_id>\d+)/$', 'ventasnorte.caja.views.detalle_usuario', name='detalle_usuario'),

    url(r'^venta_casa/(?P<casa_id>\d+)/$', 'ventasnorte.caja.views.venta_casa', name='venta_casa'),
    url(r'^venta_auto/(?P<auto_id>\d+)/$', 'ventasnorte.caja.views.venta_auto', name='venta_auto'),
    url(r'^mostrar_ticket/(?P<venta_id>\d+)/$', 'ventasnorte.caja.views.display_ticket', name='ticket'),
    url(r'^consultar_paquete/$', 'ventasnorte.caja.views.paquetes_consultar', name='consultar_paquetes'),
)

