from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^combo_dependiente/$', 'lugares.views.combo_dependiente', name='combo_em'),
)

