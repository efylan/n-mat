from django import template
#from clasificados.models import MarcaAuto, ModeloAuto, CategoriaCasa, DISPO_DICT
from clasificados.forms import CasaSimpleSearchForm, AutoSimpleSearchForm
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag()
def simple_search_casa():
    f = CasaSimpleSearchForm()

    return render_to_string('casas/form_container.html', {'form':f})

@register.simple_tag()
def simple_search_auto():
    f = AutoSimpleSearchForm()

    return render_to_string('autos/form_container.html', {'form':f})


