from django import template
from clasificados.models import MarcaAuto, ModeloAuto, CategoriaCasa, DISPO_DICT
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag()
def menu_autos():
    marcas = MarcaAuto.objects.all()
    return render_to_string('mnu_autos.html', {'marcas':marcas})


@register.simple_tag()
def menu_casas():
    categorias = CategoriaCasa.objects.all()    
    return render_to_string('mnu_casas.html', {'categorias':categorias, 'dispos':DISPO_DICT})

