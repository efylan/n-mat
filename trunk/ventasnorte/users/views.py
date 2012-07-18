# coding: latin1
from django.shortcuts import HttpResponseRedirect, render_to_response
from users.forms import LoginForm, PasswordChangeForm, CrearCasaForm, CrearAutoForm, DisplayUserForm
from users.models import Profile
from django.core.files.base import ContentFile
from django.template import RequestContext
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from clasificados.models import ClasifCasa, ClasifAuto, FotoCasa, FotoAuto
from caja.forms import PhotoForm
from caja.models import Venta
import datetime

def login(request):
    f = LoginForm()
    if request.POST:
        f = LoginForm(request.POST)
        if f.errors:
            return render_to_response('login.html', {'form':f}, RequestContext(request))
        else:
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    try:
                        a=1
                        #user.get_profile()
                    except Profile.DoesNotExist:
                        mensaje = "Usuario sin perfil. Contactar al administrador."
                        messages.error(request,mensaje)
                        return render_to_response('login.html', {'form':f, 'mensaje':mensaje}, RequestContext(request))
                    auth.login(request, user)
                    if user.is_staff:
                        return HttpResponseRedirect('/caja/panel/')
                    next=request.GET['next']
                    return HttpResponseRedirect('%s'%next)

                else:
                    mensaje = "Usuario desactivado."
                    messages.error(request,mensaje)
                    return render_to_response('login.html', {'form':f, 'mensaje':mensaje}, 
RequestContext(request))
            else:
                mensaje = "Nombre de usuario o contraseña incorrectos."
                messages.error(request,mensaje)
                return render_to_response('login.html', {'form':f,'mensaje':mensaje}, RequestContext(request))


    else:
        return render_to_response('login.html', {'form':f}, RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
    
@login_required
def panel(request):
    return render_to_response("user_panel.html", {}, RequestContext(request))


@login_required
def password_change(request):
    f=PasswordChangeForm()
    template="password_change.html"
    if request.POST:
        f=PasswordChangeForm(request.POST)
        password=request.POST['password']
        new_password=request.POST['new_password']
        username=request.user.username
        user = auth.authenticate(username=request.user.username, password=password)

        if f.errors:
            return render_to_response(template,{'form':f},RequestContext(request))			
        else:
            if  user is not None and user.is_authenticated() and user.is_active:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Su Contraseña ha sido actualizada.')
                return HttpResponseRedirect('/usuarios/panel/')
            else:
                messages.error(request, "Su Contraseña no es correcta.")
                return render_to_response(template,{'form':f},RequestContext(request))
    else:
        return render_to_response(template,{'form':f}, RequestContext(request))

@login_required
def mis_clasificados(request):
    user=request.user
    casas = user.clasifcasa_set.all()
    autos = user.clasifauto_set.all()
    return render_to_response('mis_clasificados.html', {'autos':autos,'casas':casas}, RequestContext(request))


@login_required
def mis_favoritos(request):
    user=request.user
    profile = user.get_profile()
    casas = profile.fav_casas.all()
    autos = profile.fav_autos.all()
    return render_to_response('mis_favoritos.html', {'autos':autos,'casas':casas}, RequestContext(request))

@login_required
def ver_miauto(request, auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
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

    return render_to_response('mi_auto.html',{'auto':auto,'fav_exists':fav_exists},RequestContext(request))

@login_required
def ver_micasa(request, casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
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
    return render_to_response('mi_casa.html',{'casa':casa, 'fav_exists':fav_exists},RequestContext(request))


def reactivar_casa(request, casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request,'El clasificado con ID %sc no existe' % casa_id)
        return HttpResponseRedirect('/casas/')
    if request.POST:
        if request.user.id != casa.user.id:
            messages.error(request, "No tiene autorizacion para esta accion.")
            return HttpResponseRedirect('/usuarios/panel/')        
        casa.status=0
        casa.save()
        messages.success(request, "Clasificado %sc REACTIVADO (solo por el tiempo estipulado en el paquete)." % casa_id)
    return HttpResponseRedirect('/usuarios/mi_casa/%s/'%casa_id)

def reactivar_auto(request, auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request,'El clasificado con ID %sa no existe' % auto_id)
        return HttpResponseRedirect('/autos/')
    if request.POST:
        if request.user.id != auto.user.id:
            messages.error(request, "No tiene autorizacion para esta accion.")
            return HttpResponseRedirect('/usuarios/panel/')        

        auto.status=0
        auto.save()
        messages.success(request, "Clasificado %sc REACTIVADO (solo por el tiempo estipulado en el paquete)." % auto_id)
    return HttpResponseRedirect('/usuarios/mi_auto/%s/'%auto_id)


def crear_auto(request):
    if request.POST:
        f=CrearAutoForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores')
            return render_to_response("crear_clasif_auto.html", {'form':f}, RequestContext(request))
        else:
            auto=f.save(commit=False)
            auto.status=3
            user = request.user
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
            return HttpResponseRedirect('/users/review_auto/%s/' % auto.id)
    else:
        f=CrearAutoForm()
        f2=DisplayUserForm(None)

    return render_to_response("crear_clasif_auto.html", {'form':f,'form2':f2}, RequestContext(request))


@login_required
def crear_casa(request):
    if request.POST:
        f=CrearCasaForm(request.POST)
        f2=DisplayUserForm(None, request.POST)
        if f.errors or f2.errors:
            messages.error(request, 'El formulario contiene errores')
            return render_to_response("crear_clasif_casa.html", {'form':f,'form2':f2}, RequestContext(request))
        else:
            casa=f.save(commit=False)
            casa.status=3

            casa.user = request.user
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
            return HttpResponseRedirect('/usuarios/review_casa/%s/' % casa.id)
    else:
        f=CrearCasaForm()
        f2=DisplayUserForm(request.user)

    return render_to_response("crear_clasif_casa.html", {'form':f, 'form2':f2}, RequestContext(request))


@login_required
def review_casa(request,casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request, 'El clasificado No. %sc no existe.'%casa_id)
        return HttpResponseRedirect('/users/panel/')

    if request.user.id != casa.user.id:
        messages.error(request, "Clasificado con ID no es de su propiedad." % casa_id)
        return Http404()

    f = PhotoForm(casa)
    return render_to_response('review_casa_usr.html',{'casa':casa, 'form':f},RequestContext(request))


@login_required
def review_auto(request,auto_id):
    try:
        auto=ClasifAuto.objects.get(id=auto_id)
    except ClasifAuto.DoesNotExist:
        messages.error(request, 'El clasificado No. %sa no existe.'%auto_id)
        return HttpResponseRedirect('/users/panel/')

    if request.user.id != auto.user.id:
        messages.error(request, "Clasificado con ID no es de su propiedad." % casa_id)
        return Http404()

    f = PhotoForm(auto)
    return render_to_response('review_auto.html',{'auto':auto,'form':f},RequestContext(request))


def venta_casa(request, casa_id):
    try:
        casa = ClasifCasa.objects.get(id=casa_id)
    except:
        messages.error(request, "Clasificado con ID %sc no encontrado" % casa_id)
        return HttpResponseRedirect('/caja/panel/')

    if request.user.id != casa.user.id:
        messages.error(request, "Clasificado con ID no es de su propiedad." % casa_id)
        return Http404()
    
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
        return HttpResponseRedirect('/users/panel/')


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


def editar_casa(request, casa_id):
    try:
        casa_i = ClasifCasa.objects.get(id=casa_id)
        paquete = casa_i.paquete
    except:
        messages.error(request, "Clasificado con ID %sc no encontrado" % casa_id)
        return HttpResponseRedirect('/usuarios/panel/')

    if request.POST:
        f=CrearCasaForm(request.POST, instance=casa_i)
        f2=DisplayUserForm(None, request.POST)
        if f.errors or f2.errors:
            messages.error(request, 'El formulario contiene errores')
            return render_to_response("crear_clasif_casa.html", {'form':f,'form2':f2}, RequestContext(request))
        else:
            casa=f.save(commit=False)

            if casa.status == 1 or casa.status == 0:
                casa.paquete = paquete

            user = request.user

            casa.user = user
            casa.email = f2.cleaned_data['email']
            casa.telefono = f2.cleaned_data['phone_number']
            casa.celular = f2.cleaned_data['cellphone']
            casa.direccion = f2.cleaned_data['address'] 

            casa.save()

            messages.success(request, 'Clasificado editado con exito')
            return HttpResponseRedirect('/usuarios/review_casa/%s/' % casa.id)
    else:
        f=CrearCasaForm(instance=casa_i)
        f2=DisplayUserForm(request.user)

    return render_to_response("crear_clasif_casa.html", {'form':f,'form2':f2}, RequestContext(request))

@login_required
def agregar_fotos_casa(request,casa_id):
    try:
        casa=ClasifCasa.objects.get(id=casa_id)
    except ClasifCasa.DoesNotExist:
        messages.error(request, 'El clasificado No. %sc no existe.'%casa_id)
        return HttpResponseRedirect('/usuarios/panel/')
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
                
            return HttpResponseRedirect('/usuarios/review_casa/%s/'%casa.id)
    else:
        return render_to_response('review_casa.html',{'casa':casa, 'form':f},RequestContext(request))



@login_required
def eliminar_foto_casa(request, foto_id):
    try:
        foto = FotoCasa.objects.get(id=foto_id)
    except:
        messages.error(request,'La imagen no existe.')
        return HttpResponseRedirect('/usuarios/panel/')
    if request.POST:
        casa = foto.casa.id
        foto.foto.delete()
        foto.delete()
        messages.error(request,'La imagen fue eliminada exitosamente.')
        return HttpResponseRedirect('/usuarios/review_casa/%s/'%casa)

@login_required
def foto_prin_casa(request, foto_id):
    try:
        foto = FotoCasa.objects.get(id=foto_id)
    except:
        messages.error(request,'La imagen no existe.')
        return HttpResponseRedirect('/usuarios/panel/')
    if request.POST:
        casa = foto.casa.id
        foto.principal=True
        foto.save()
        messages.success(request,'La imagen fue seleccionada como PRINCIPAL.')
        return HttpResponseRedirect('/usuarios/review_casa/%s/'%casa)

