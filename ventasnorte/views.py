from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext

def index(request):
    empresa = 'Ventas del Norte'
    #TODO extraer de config
    return render_to_response("index.html", {"empresa":empresa}, RequestContext(request))
