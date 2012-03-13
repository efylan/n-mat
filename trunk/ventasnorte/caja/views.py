# coding: latin1
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.core.files.base import ContentFile
from clasificados.models import ClasifCasa, ClasifAuto, FotoCasa, FotoAuto, Paquete
from caja.forms import CrearCasaForm, CrearAutoForm, DisplayUserForm, PhotoForm, IdForm, NameSearchForm
from caja.models import Venta
from users.forms import RegistrationForm
from django.contrib import messages
from ventasnorte.utils import get_pronounceable_password
from django.contrib.auth.models import User
from users.models import Profile, CLIENTE
import simplejson
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Q

@login_required
def registrar_usuario(request):
    if request.POST:
        f=RegistrationForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores')
            return render_to_response("registro_caja.html", {'form':f}, RequestContext(request))
        else:
            data = f.cleaned_data
            user=User()
            user.username=data["username"]
            passwd=get_pronounceable_password(1,2)
            user.set_password(passwd)
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

            profile = Profile()
            profile.user=user
            profile.telefono = data['phone_number']
            profile.celular = data['cellphone']
            profile.direccion = data['address']
            profile.tipo = CLIENTE
            profile.save()
            
            messages.success(request, 'Usuario creado con exito')

            return render_to_response('mostrar_usuario.html', {'user':user,'passwd':passwd}, RequestContext(request))

    else:
        f=RegistrationForm()

    return render_to_response("registro_caja.html", {'form':f}, RequestContext(request))

@login_required    
def mostrar_usuario(request):
    user={'username':'pruebaza','id':'999'}
    passwd='asdf43'
    return render_to_response('mostrar_usuario.html',{'user':user, 'passwd':passwd}, RequestContext(request))

@login_required
def panel(request):
    return render_to_response("panel.html", {}, RequestContext(request))

@login_required
def crear_ccasa(request):
    if request.POST:
        f=CrearCasaForm(request.POST)
        f2=DisplayUserForm(None, request.POST)
        if f.errors or f2.errors:
            messages.error(request, 'El formulario contiene errores')
            return render_to_response("crear_clasif_casa.html", {'form':f,'form2':f2}, RequestContext(request))
        else:
            casa=f.save(commit=False)
            casa.status=3

            id_user = f.cleaned_data['userid']
            user = User.objects.get(id=id_user)

            casa.user = user
            casa.email = f2.cleaned_data['email']
            casa.telefono = f2.cleaned_data['phone_number']
            casa.celular = f2.cleaned_data['cellphone']
            casa.direccion = f2.cleaned_data['address'] 
            hoy = datetime.date.today()
            casa.fecha_inicio = hoy
            delta = datetime.timedelta(days=casa.paquete.dias_activo)
            casa.fecha_fin = hoy + delta
            casa.usuario_creador = request.user
            casa.save()

            messages.success(request, 'Clasificado creado con exito')
            return HttpResponseRedirect('/caja/review_casa/%s/' % casa.id)
    else:
        f=CrearCasaForm()
        f2=DisplayUserForm()

    return render_to_response("crear_clasif_casa.html", {'form':f,'form2':f2}, RequestContext(request))

@login_required
def crear_cauto(request):
    if request.POST:
        f=CrearAutoForm(request.POST)
        f2=DisplayUserForm(None, request.POST)
        if f.errors or f2.errors:
            messages.error(request, 'El formulario contiene errores')
            return render_to_response("crear_clasif_auto.html", {'form':f,'form2':f2}, RequestContext(request))
        else:
            auto=f.save(commit=False)
            auto.status=3
            id_user = f.cleaned_data['userid']
            user = User.objects.get(id=id_user)
            auto.user = user
            auto.email = f2.cleaned_data['email']
            auto.telefono = f2.cleaned_data['phone_number']
            auto.celular = f2.cleaned_data['cellphone']
            auto.direccion = f2.cleaned_data['address'] 
            hoy = datetime.date.today()

            auto.usuario_creador = request.user
            auto.fecha_inicio = hoy
            delta = datetime.timedelta(days=auto.paquete.dias_activo)
            auto.fecha_fin = hoy + delta

            auto.save()

            messages.success(request, 'Clasificado creado con exito')
            return HttpResponseRedirect('/caja/review_auto/%s/' % auto.id)
    else:
        f=CrearAutoForm()
        f2=DisplayUserForm(None)

    return render_to_response("crear_clasif_auto.html", {'form':f,'form2':f2}, RequestContext(request))

@login_required
def review_casa(request,casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request, 'El clasificado No. %sc no existe.'%casa_id)
        return HttpResponseRedirect('/caja/panel/')
    f = PhotoForm(casa)
    return render_to_response('review_casa.html',{'casa':casa, 'form':f},RequestContext(request))

@login_required
def review_auto(request,auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request, 'El clasificado No. %sa no existe.'%auto_id)
        return HttpResponseRedirect('/caja/panel/')
    f = PhotoForm(auto)
    return render_to_response('review_auto.html',{'auto':auto,'form':f},RequestContext(request))

@login_required
def usuarios_consultar(request):
    if request.POST:
        user_id=request.POST['elegido']
        if not user_id== '':
            try:
                user = User.objects.get(id = user_id)
                profile = user.get_profile()              
            except User.DoesNotExist:
                return HttpResponseNotFound()


            to_return={}
            to_return['username'] = user.username
            to_return['first_name'] = user.first_name
            to_return['last_name'] = user.last_name
            to_return['email'] = user.email
            to_return['phone_number'] = profile.telefono
            to_return['cellphone'] = profile.celular
            to_return['address'] = profile.direccion
            serialized = simplejson.dumps(to_return)

            return HttpResponse(serialized, mimetype="application/json")
#            return render_to_response("nombre_usuario.txt", {'user':user})
    else:
        return HttpResponseNotFound()

@login_required
def agregar_fotos_casa(request,casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request, 'El clasificado No. %sc no existe.'%casa_id)
        return HttpResponseRedirect('/caja/panel/')
    f = PhotoForm(casa)
    if request.POST:
        f = PhotoForm(casa, request.POST,request.FILES)
        if f.errors:
            return render_to_response('review_casa.html',{'casa':casa, 'form':f},RequestContext(request))
        else:
            for key in request.FILES.keys():
                imagen=request.FILES[key]                
                fotocasa=FotoCasa()
                if key == "main_picture":
                    print "MAIN"
                    fotocasa.principal=True
                else:
                    fotocasa.principal=False
                fotocasa.casa=casa
                img_content = ContentFile(imagen.read()) 
                fotocasa.foto.save(imagen.name, img_content)
                fotocasa.save()
                
            return HttpResponseRedirect('/caja/review_casa/%s/'%casa.id)
    else:
        return render_to_response('review_casa.html',{'casa':casa, 'form':f},RequestContext(request))


@login_required
def agregar_fotos_auto(request,auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request, 'El clasificado No. %sa no existe.'%casa_id)
        return HttpResponseRedirect('/caja/panel/')
    f = PhotoForm(auto)
    if request.POST:
        f = PhotoForm(auto, request.POST,request.FILES)
        if f.errors:
            return render_to_response('review_auto.html',{'auto':auto, 'form':f},RequestContext(request))
        else:
            for key in request.FILES.keys():
                imagen=request.FILES[key]
                fotoauto=FotoAuto()
                if key == "main_picture":
                    print "MAIN"
                    fotoauto.principal=True
                else:
                    fotoauto.principal=False
                fotoauto.auto=auto
                img_content = ContentFile(imagen.read()) 
                fotoauto.foto.save(imagen.name, img_content)
                fotoauto.save()
                
            return HttpResponseRedirect('/caja/review_auto/%s/'%auto.id)
    else:
        return render_to_response('review_auto.html',{'auto':auto, 'form':f},RequestContext(request))

@login_required
def editar_casa(request, casa_id):
    try:
        casa = ClasifCasa.objects.get(id=casa_id)
    except:
        messages.error(request, "Clasificado con ID %sc no encontrado" % casa_id)
        return HttpResponseRedirect('/caja/panel/')

    if request.POST:
        f=CrearCasaForm(request.POST, instance=casa)
        f2=DisplayUserForm(None, request.POST)
        if f.errors or f2.errors:
            messages.error(request, 'El formulario contiene errores')
            return render_to_response("crear_clasif_casa.html", {'form':f,'form2':f2}, RequestContext(request))
        else:
            casa=f.save(commit=False)

            id_user = f.cleaned_data['userid']
            user = User.objects.get(id=id_user)

            casa.user = user
            casa.email = f2.cleaned_data['email']
            casa.telefono = f2.cleaned_data['phone_number']
            casa.celular = f2.cleaned_data['cellphone']
            casa.direccion = f2.cleaned_data['address'] 

            casa.save()

            messages.success(request, 'Clasificado editado con exito')
            return HttpResponseRedirect('/caja/review_casa/%s/' % casa.id)
    else:
        f=CrearCasaForm(instance=casa)
        f2=DisplayUserForm(casa)

    return render_to_response("crear_clasif_casa.html", {'form':f,'form2':f2}, RequestContext(request))


@login_required
def editar_auto(request, auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request,'El clasificado con ID %sa no existe' % auto_id)
        return HttpResponseRedirect('/caja/panel/')
    if request.POST:
        f=CrearAutoForm(request.POST, instance=auto)
        f2=DisplayUserForm(None, request.POST)
        if f.errors or f2.errors:
            messages.error(request, 'El formulario contiene errores')
            return render_to_response("crear_clasif_auto.html", {'form':f,'form2':f2}, RequestContext(request))
        else:
            auto=f.save(commit=False)
            id_user = f.cleaned_data['userid']
            user = User.objects.get(id=id_user)
            auto.user = user
            auto.email = f2.cleaned_data['email']
            auto.telefono = f2.cleaned_data['phone_number']
            auto.celular = f2.cleaned_data['cellphone']
            auto.direccion = f2.cleaned_data['address'] 

            auto.save()

            messages.success(request, 'Clasificado editado con exito')
            return HttpResponseRedirect('/caja/review_auto/%s/' % auto.id)
    else:
        f=CrearAutoForm(instance=auto)
        f2=DisplayUserForm(auto)

    return render_to_response("crear_clasif_auto.html", {'form':f,'form2':f2}, RequestContext(request))

@login_required
def eliminar_foto_casa(request, foto_id):
    try:
        foto = FotoCasa.objects.get(id=foto_id)
    except:
        messages.error(request,'La imagen no existe.')
        return HttpResponseRedirect('/caja/panel/')
    if request.POST:
        casa = foto.casa.id
        foto.foto.delete()
        foto.delete()
        messages.error(request,'La imagen fue eliminada exitosamente.')
        return HttpResponseRedirect('/caja/review_casa/%s/'%casa)

@login_required
def eliminar_foto_auto(request, foto_id):
    try:
        foto = FotoAuto.objects.get(id=foto_id)
    except:
        messages.error(request,'La imagen no existe.')
        return HttpResponseRedirect('/caja/panel/')
    if request.POST:
        auto = foto.auto.id
        foto.foto.delete()
        foto.delete()
        messages.error(request,'La imagen fue eliminada exitosamente.')
        return HttpResponseRedirect('/caja/review_auto/%s/'%auto)

@login_required
def foto_prin_casa(request, foto_id):
    try:
        foto = FotoCasa.objects.get(id=foto_id)
    except:
        messages.error(request,'La imagen no existe.')
        return HttpResponseRedirect('/caja/panel/')
    if request.POST:
        casa = foto.casa.id
        foto.principal=True
        foto.save()
        messages.success(request,'La imagen fue seleccionada como PRINCIPAL.')
        return HttpResponseRedirect('/caja/review_casa/%s/'%casa)

@login_required
def foto_prin_auto(request, foto_id):
    try:
        foto = FotoAuto.objects.get(id=foto_id)
    except:
        messages.error(request,'La imagen no existe.')
        return HttpResponseRedirect('/caja/panel/')
    if request.POST:
        auto = foto.auto.id
        foto.principal=True
        foto.save()
        messages.error(request,'La imagen fue seleccionada como PRINCIPAL.')
        return HttpResponseRedirect('/caja/review_auto/%s/'%auto)



@login_required
def modificaciones(request):
    f1=IdForm()
    f2=NameSearchForm()
    return render_to_response('edicion/modificaciones.html', {'f1':f1,'f2':f2}, RequestContext(request))

@login_required
def id_search(request):
    if request.POST:
        f = IdForm(request.POST)
        if f.errors:
            f2 = NameSearchForm()
            return render_to_response("edicion/modificaciones.html",{'f1':f, 'f2':f2},RequestContext(request))
        else:
            search_id = f.cleaned_data['search_id']
            tipo = f.cleaned_data['tipo']
            print tipo, type(tipo)
            if tipo == "1":
                print "entra auto"
                try:
                    auto = ClasifAuto.objects.get(id=search_id)
                except ClasifAuto.DoesNotExist:
                    messages.error(request, "El clasificado con ID %sa no existe." % search_id)
                    return HttpResponseRedirect('/caja/modificaciones/')
                return HttpResponseRedirect('/caja/editar_auto/%s/' % search_id)
            else:
                print "entra casa"
                try:
                    auto = ClasifCasa.objects.get(id=search_id)
                except ClasifCasa.DoesNotExist:
                    messages.error(request, "El clasificado con ID %sc no existe." % search_id)
                    return HttpResponseRedirect('/caja/modificaciones/')
                return HttpResponseRedirect('/caja/editar_casa/%s/' % search_id)
          

@login_required
def name_search(request):
    if request.GET:
        f = NameSearchForm(request.GET)
        if f.errors:
            f1 = IdForm()
            return render_to_response("edicion/modificaciones.html",{'f1':f1, 'f2':f},RequestContext(request))
        else:
            user_id = f.cleaned_data['id_user']
            username = f.cleaned_data['username']
            name = f.cleaned_data['name']
            last_name = f.cleaned_data['last_name']

            query = Q()
            print user_id
            print username
            print name
            print last_name

            if user_id != None:
                if user_id != '':
                    query = query | Q(id=user_id)
            if username != None:
                if username != '':
                    query = query | Q(username__icontains=username)
            if name !=None:
                if name != '':
                    query = query | Q(first_name__icontains=name)
            if last_name !=None:
                if last_name != '':
                    query = query | Q(last_name__icontains=last_name)

            users = User.objects.filter(query)

            return render_to_response('edicion/user_list.html',{"users":users}, RequestContext(request))

    else:
        users = User.objects.none()

        return render_to_response('edicion/user_list.html',{"users":users}, RequestContext(request))


@login_required
def detalle_usuario(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request,'El usuario con ID %s no existe.' % user_id)
        return HttpResponseRedirect('/caja/modificaciones/')
    
    autos = user.clasifauto_set.all().order_by('-fecha_creacion')
    casas = user.clasifcasa_set.all().order_by('-fecha_creacion')
    return render_to_response('edicion/user_details.html',{'user':user,'autos':autos, 'casas':casas})

def venta_casa(request, casa_id):
    try:
        casa = ClasifCasa.objects.get(id=casa_id)
    except:
        messages.error(request, "Clasificado con ID %sc no encontrado" % casa_id)
        return HttpResponseRedirect('/caja/panel/')
    if request.POST:
        if casa.status == 0:
            messages.error(request, "Clasificado con ID %sc vendido con anterioridad" % casa_id)
            return HttpResponseRedirect('/caja/panel/')
            
        venta = Venta()
        paquete = casa.paquete
        venta.paquete = paquete
        venta.nombre_paquete = paquete.nombre
        venta.precio_paquete = paquete.precio
        venta.precio_prioridad = paquete.prioridad
        venta.precio_foto = paquete.foto_extra
        venta.precio_texto = paquete.texto_extra
        venta.min_fotos = paquete.min_fotos
        venta.min_texto = paquete.min_texto

        num_fotos_extra = casa.get_extra_photo_count()
        venta.fotos_extra = num_fotos_extra

        texto_extra = casa.has_extra_text()
        venta.texto_extra = texto_extra
        venta.prioridad = casa.prioridad

        venta.total = casa.get_total()
        venta.tipo = 2
        venta.casa = casa

        venta.save()

        casa.status = 0
        casa.save()
        return HttpResponseRedirect('/caja/mostrar_ticket/%s/'%venta.id)
    else:
        messages.error(request, "Sin accion tomada. No se realizo la venta.")
        return HttpResponseRedirect('/caja/panel/')

def venta_auto(request, auto_id):
    try:
        auto = ClasifAuto.objects.get(id=auto_id)
    except:
        messages.error(request, "Clasificado con ID %sa no encontrado" % auto_id)
        return HttpResponseRedirect('/caja/panel/')
    if request.POST:
        if auto.status == 0:
            messages.error(request, "Clasificado con ID %sa vendido con anterioridad" % auto_id)
            return HttpResponseRedirect('/caja/panel/')
            
        venta = Venta()
        paquete = auto.paquete
        venta.paquete = paquete
        venta.nombre_paquete = paquete.nombre
        venta.precio_paquete = paquete.precio
        venta.precio_prioridad = paquete.prioridad
        venta.precio_foto = paquete.foto_extra
        venta.precio_texto = paquete.texto_extra
        venta.min_fotos = paquete.min_fotos
        venta.min_texto = paquete.min_texto

        num_fotos_extra = auto.get_extra_photo_count()
        venta.fotos_extra = num_fotos_extra

        texto_extra = auto.has_extra_text()
        venta.texto_extra = texto_extra
        venta.prioridad = auto.prioridad

        venta.total = auto.get_total()
        venta.tipo = 1
        venta.auto = auto

        venta.save()

        auto.status = 0
        auto.save()
        return HttpResponseRedirect('/caja/mostrar_ticket/%s/'%venta.id)
    else:
        messages.error(request, "Sin accion tomada. No se realizo la venta.")
        return HttpResponseRedirect('/caja/panel/')


def display_ticket(request, venta_id):
    try:
        venta = Venta.objects.get(id=venta_id)
    except Venta.DoesNotExist:
        request.error(request, 'La venta con ID %s no existe' % venta_id)
    clasif = venta.get_clasificado()
    user = clasif.user
    return render_to_response('ticket.html', {'venta':venta, 'clasif':clasif, 'user':user}, RequestContext(request))


@login_required
def paquetes_consultar(request):
    if request.POST:
        paquete_id=request.POST['elegido']
        if not paquete_id== '':
            try:
                paquete = Paquete.objects.get(id = paquete_id)
            except User.DoesNotExist:
                return HttpResponseNotFound()


            to_return={}
            to_return['min_texto'] = paquete.min_texto
            serialized = simplejson.dumps(to_return)

            return HttpResponse(serialized, mimetype="application/json")
#            return render_to_response("nombre_usuario.txt", {'user':user})
    else:
        return HttpResponseNotFound()

