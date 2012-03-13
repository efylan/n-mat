from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.core.files.base import ContentFile
from clasificados.models import ClasifCasa, ClasifAuto, FotoCasa, FotoAuto, MarcaAuto, ModeloAuto, CategoriaCasa, DISPO_DICT
from clasificados.forms import CasaSimpleSearchForm, AutoSimpleSearchForm
from caja.forms import CrearCasaForm, CrearAutoForm, DisplayUserForm, PhotoForm
from users.forms import RegistrationForm
from django.contrib import messages
from ventasnorte.utils import get_pronounceable_password, get_query
from django.contrib.auth.models import User
from users.models import Profile, CLIENTE
import simplejson
from django.db.models import Q

def main_autos(request):
    autos=ClasifAuto.get_actives.all()
    return render_to_response('autos/main_autos.html',{'autos':autos},RequestContext(request))

def main_casas(request):
    casas=ClasifCasa.get_actives.all()
    return render_to_response('casas/main_casas.html',{'casas':casas},RequestContext(request))

def ver_auto(request, auto_id):
    try:
        auto=ClasifAuto.get_actives.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request,'El clasificado con ID %sa no existe' % auto_id)
        return HttpResponseRedirect('/autos/')

    if request.user.id:
        try:
            profile = request.user.get_profile()
            if auto in profile.fav_autos.all():
                fav_exists = True
            else:
                fav_exists = False
        except Profile.DoesNotExist:
            pass
            fav_exists=False
    else:
        fav_exists=False

    return render_to_response('autos/detalle_auto.html',{'auto':auto,'fav_exists':fav_exists},RequestContext(request))


def ver_casa(request, casa_id):
    try:
        casa=ClasifCasa.get_actives.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request,'El clasificado con ID %sc no existe' % casa_id)
        return HttpResponseRedirect('/casas/')
    if request.user.id:
        try:
            profile = request.user.get_profile()
            if casa in profile.fav_casas.all():
                fav_exists = True
            else:
                fav_exists = False
        except Profile.DoesNotExist:
            pass
            fav_exists=False
    else:
        fav_exists=False

    return render_to_response('casas/detalle_casa.html',{'casa':casa, 'fav_exists':fav_exists},RequestContext(request))


def fav_casa(request, casa_id):
    try:
        casa=ClasifCasa.get_actives.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request,'El clasificado con ID %sc no existe' % casa_id)
        return HttpResponseRedirect('/casas/')
    if request.POST:
        profile=request.user.get_profile()
        profile.fav_casas.add(casa)
        messages.success(request, "Clasificado %sc agregado a Favoritos" % casa_id)
    return HttpResponseRedirect('/casas/detalle_casa/%s/' % casa_id)

def fav_auto(request, auto_id):
    try:
        auto=ClasifAuto.get_actives.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request,'El clasificado con ID %sa no existe' % auto_id)
        return HttpResponseRedirect('/autos/')
    if request.POST:
        profile=request.user.get_profile()
        profile.fav_autos.add(auto)
        messages.success(request, "Clasificado %sa agregado a Favoritos" % auto_id)
    return HttpResponseRedirect('/autos/detalle_auto/%s/' % auto_id)

def rmfav_casa(request, casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request,'El clasificado con ID %sc no existe' % casa_id)
        return HttpResponseRedirect('/casas/')
    if request.POST:
        profile=request.user.get_profile()
        profile.fav_casas.remove(casa)
        messages.success(request, "Clasificado %sc quitado de Favoritos" % casa_id)
    return HttpResponseRedirect('/casas/detalle_casa/%s/' % casa_id)

def rmfav_auto(request, auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request,'El clasificado con ID %sa no existe' % auto_id)
        return HttpResponseRedirect('/autos/')
    if request.POST:
        profile=request.user.get_profile()
        profile.fav_autos.remove(auto)
        messages.success(request, "Clasificado %sa quitado de Favoritos" % auto_id)
    return HttpResponseRedirect('/autos/detalle_auto/%s/' % auto_id)

def apagar_casa(request, casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request,'El clasificado con ID %sc no existe' % casa_id)
        return HttpResponseRedirect('/casas/')
    if request.POST:
        casa.status=1
        casa.save()
        messages.error(request, "Clasificado %sc DESACTIVADO, para reactivarlo (solo por el tiempo estipulado en el paquete) vaya a la seccion de Mis Clasificados en el panel de usuario." % casa_id)
    return HttpResponseRedirect('/usuarios/panel/')

def apagar_auto(request, auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request,'El clasificado con ID %sa no existe' % auto_id)
        return HttpResponseRedirect('/autos/')
    if request.POST:
        auto.status=1
        auto.save()
        messages.error(request, "Clasificado %sc DESACTIVADO, para reactivarlo (solo por el tiempo estipulado en el paquete) vaya a la seccion de Mis Clasificados en el panel de usuario." % auto_id)
    return HttpResponseRedirect('/usuarios/panel/')


def marcas_autos(request):
    marcas=MarcaAuto.objects.all()
    return render_to_response('autos/marcas_autos.html', {'marcas':marcas}, RequestContext(request))

def modelos_autos(request, marca_slug):
    marca = MarcaAuto.objects.get(slug=marca_slug)
    modelos = marca.modeloauto_set.all()
    return render_to_response('autos/modelos_autos.html', {'marca':marca,'modelos':modelos}, RequestContext(request))

def series_autos(request, modelo_slug):
    modelo = ModeloAuto.objects.get(slug=modelo_slug)
    autos = ClasifAuto.get_actives.filter(modelo=modelo)
    return render_to_response('autos/series_autos.html', {'modelo':modelo, 'autos':autos}, RequestContext(request))

def categorias_casas(request):
    categorias = CategoriaCasa.objects.all()
    return render_to_response('casas/categorias_casas.html', {'categorias':categorias}, RequestContext(request))

def disponibilidad_casas(request, categoria_slug):
    categoria = CategoriaCasa.objects.get(slug=categoria_slug)
    dispos= DISPO_DICT

    return render_to_response('casas/disponibilidad_casas.html', {'categoria':categoria, 'dispos':dispos}, RequestContext(request))

def catdis_casas(request, categoria_slug, dispo_slug):
    categoria = CategoriaCasa.objects.get(slug=categoria_slug)
    dispos = DISPO_DICT    
    for disp in dispos:
        if disp['slug'] == dispo_slug:
            dispo=disp
    casas = ClasifCasa.get_actives.filter(categoria_casa=categoria, disponibilidad=dispo['id'])
    return render_to_response('casas/catdis_casas.html', {'categoria':categoria, 'dispo':dispo, 'casas':casas}, RequestContext(request))


def simple_search_casas(request):
    if request.GET:
        f = CasaSimpleSearchForm(request.GET)
        if f.errors:
            casas = []
            return render_to_response('casas/simple_search.html',{'form':f}, RequestContext(request))
        else:
            dispo = f.cleaned_data['disponibilidad']
            cate = f.cleaned_data['categoria']
            estado = f.cleaned_data['estado']
            muni = f.cleaned_data['municipio']
            cond = f.cleaned_data['condicion']

            query = Q()
            if dispo != '':
                print dispo, "dispo"
                query = query & Q(disponibilidad = dispo)

            if cate != None:
                print cate, "cate"
                query = query & Q(categoria_casa = cate)

            if estado != None:
                print estado, "edo"
                query = query & Q(estado = estado)

            if muni != None:
                print muni, "muni"
                query = query & Q(municipio = muni)

            if cond != '':
                print cond, "cond", type(cond), cond == None
                query = query & Q(condicion = cond)

            casas = ClasifCasa.get_actives.filter(query)
            
            return render_to_response('casas/search_results.html',{'casas':casas,'form':f},RequestContext(request))
    else:    
        f=CasaSimpleSearchForm()
        return render_to_response('casas/simple_search.html',{'form':f}, RequestContext(request))
        




def simple_search_autos(request):
    if request.GET:
        f = AutoSimpleSearchForm(request.GET)
        if f.errors:
            casas = []
            return render_to_response('casas/simple_search.html',{'form':f}, RequestContext(request))
        else:
            marca = f.cleaned_data['marca']
            modelo = f.cleaned_data['modelo']
            serie = f.cleaned_data['serie']
            trans = f.cleaned_data['transmision']
            estado = f.cleaned_data['estado']
            muni = f.cleaned_data['municipio']

            query = Q()
            if marca != None:
                print marca, "marca"
                query = query & Q(marca = marca)

            if modelo != None:
                print modelo, "modelo"
                query = query & Q(modelo = modelo)

            if serie != None:
                print serie, "serie"
                query = query & Q(serie = serie)

            if trans != '':
                print trans, "trans"
                query = query & Q(transmision = trans)

            if muni != None:
                print muni, "muni"
                query = query & Q(municipio = muni)


            autos = ClasifAuto.get_actives.filter(query)
            
            return render_to_response('autos/search_results.html',{'autos':autos,'form':f},RequestContext(request))
    else:    
        f=AutoSimpleSearchForm()
        return render_to_response('autos/simple_search.html',{'form':f}, RequestContext(request))






def combo_dependiente_autos(request):
	if request.POST:
		marca=request.POST['elegido']
		if not marca=='':
			modelos=ModeloAuto.objects.filter(marca__id__exact=int(marca)).order_by('nombre')
			optionlist=[{'id':'','nombre':"-Elegir Modelo-"}]
			for modelo in modelos:
				optiondict={}
				optiondict['id']=modelo.id
				#print optiondict['id']
				optiondict['nombre']=modelo.nombre
				optionlist.append(optiondict)
			return render_to_response("combo_dependiente.txt", {'options':optionlist})
		else:
			optionlist=[]
			optiondict={}
			optiondict['id']=''
			optiondict['nombre']="---------"
			optionlist.append(optiondict)
			return render_to_response("combo_dependiente.txt", {'options':optionlist})
			
	else:
		pass


def album_auto(request, auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request,'El clasificado con ID %sa no existe' % auto_id)
        return HttpResponseRedirect('/autos/')
    galeria = auto.fotoauto_set.all()
    return render_to_response('autos/galeria.html',{'galeria':galeria,'auto':auto},RequestContext(request))


def album_casa(request, casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request,'El clasificado con ID %sc no existe' % casa_id)
        return HttpResponseRedirect('/casas/')
    galeria = casa.fotocasa_set.all()
    return render_to_response('casas/galeria.html',{'galeria':galeria, 'casa':casa}, RequestContext(request))



def text_search_casa(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['titulo', 'descripcion', 'domicilio', 'condicion', 'referencia'])
        
        casas = ClasifCasa.get_actives.filter(entry_query)

    return render_to_response('casas/search_results.html',
                          { 'query_string': query_string, 'casas': casas },
                          context_instance=RequestContext(request))

def text_search_auto(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['titulo', 'descripcion', 'color', 'marca__nombre', 'modelo__nombre', 'serie__nombre'])
        
        autos = ClasifAuto.get_actives.filter(entry_query)

    return render_to_response('autos/search_results.html',
                          { 'query_string': query_string, 'autos': autos },
                          context_instance=RequestContext(request))
