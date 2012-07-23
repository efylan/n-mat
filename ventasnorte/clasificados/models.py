# coding: latin1
from django.db import models
from django.db.models import Q
from lugares.models import Estado, Municipio
from django.contrib import admin
from django.contrib.auth.models import User
from PIL import Image
import datetime
from django.template.defaultfilters import slugify

DISPO_DICT = [{'nombre':'En Venta','slug':'venta', 'id':1}, {'nombre':'En Renta','slug':'renta','id':2}, {'nombre':'Traspaso','slug':'traspaso','id':3}]

MONEDA_CHOICES = ((1, 'Pesos'),(2,'Dolares'))
CONDICION_CASA_CHOICES = ((1, 'Excelente'),(2,'Buena'),(3,'Regular'))
CONDICION_AUTO_CHOICES = ((1, 'Excelente'),(2,'Buena'),(3,'Regular'), (4,'Chocado'))
DISPO_CHOICES = ((1, 'Venta'),(2, 'Renta'),(3, 'Traspaso'))
TRANSMISION_CHOICES = ((1,'Standard'),(2,'Automatico'))
COMBUST_CHOICES = ((1, 'Gasolina'),(2,'Diesel'))
STATUS_CHOICES = ((0,'Activo'), (1, 'Vendido'), (2,'Reactivado'), (3,'Pendiente'))
NACION_CHOICES = ((1,'Mexicano'),(2,'Regularizado'),(3,'Americano'))

IMG_NOT_AVAILABLE_CASA = "/img/no_disponible_casa.png"
IMG_NOT_AVAILABLE_AUTO = "/img/no_disponible_auto.png"

class Paquete(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    dias_activo = models.IntegerField()
    min_fotos = models.IntegerField()
    min_texto = models.IntegerField(help_text="Numero de caracteres minimos.")
    foto_extra = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Precio de foto extra")
    texto_extra = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Precio de texto extra")
    prioridad = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Precio de prioridad")
    def __unicode__(self):
        return self.nombre

class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('nombre','precio', 'min_fotos','min_texto','foto_extra','texto_extra')

try:
    admin.site.register(Paquete,PaqueteAdmin)
except:
    pass

class CategoriaCasa(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(editable=False, unique=True)
    def __unicode__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug= slugify(self.nombre)
        super(CategoriaCasa, self).save(*args, **kwargs)

    def clasif_count(self):
        return self.clasifcasa_set.filter(status=0).count()

try:
    admin.site.register(CategoriaCasa)
except:
    pass


class CasaActivesManager(models.Manager):
    def get_query_set(self):
        hoy = datetime.date.today()
        return super(CasaActivesManager, self).get_query_set().filter(status=0, fecha_inicio__lte=hoy, fecha_fin__gte=hoy).order_by('-prioridad')



class ClasifCasa(models.Model):
    user = models.ForeignKey(User)
    titulo=models.CharField(max_length=70)
    paquete=models.ForeignKey(Paquete, blank=False, default='')
    precio=models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True, verbose_name="Precio de Casa")
    moneda=models.PositiveSmallIntegerField(choices=MONEDA_CHOICES, null=True, blank=True)
    disponibilidad=models.PositiveSmallIntegerField(choices=DISPO_CHOICES)
    categoria_casa = models.ForeignKey(CategoriaCasa, verbose_name="Categoria")

    estado=models.ForeignKey(Estado,blank=False, default='')
    municipio=models.ForeignKey(Municipio,blank=False, default='')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)

    domicilio=models.CharField(max_length=200, null=True, blank=True)
    colonia=models.CharField(max_length=70, null=True, blank=True)
    codigo_postal=models.IntegerField(null=True, blank=True)
    referencia=models.CharField(max_length=70, null=True, blank=True)#TODO Estara bien este?
    condicion=models.PositiveSmallIntegerField(choices=CONDICION_CASA_CHOICES)
    pisos=models.IntegerField()
    superficie=models.CharField(max_length=15, null=True, blank=True)#TODO Estara bien este?
    recamaras=models.IntegerField(null=True, blank=True)#TODO Estara bien este?
    banos=models.IntegerField(null=True, blank=True)#TODO Estara bien este?
    descripcion=models.TextField(null=True, blank=True)
    prioridad = models.BooleanField(help_text="Cargo extra por presencia en pagina principal.")
    usuario_creador = models.ForeignKey(User, related_name="creadorcasa_set")
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    fecha_creacion=models.DateTimeField(auto_now_add=True)
    fecha_modificacion=models.DateTimeField(auto_now=True)
    
    #Informacion de usuario
    email=models.EmailField(max_length=75, null=True, blank=True)
    telefono=models.CharField(max_length=30, null=True, blank=True)
    celular=models.CharField(max_length=30, null=True, blank=True)
    direccion=models.TextField(null=True, blank=True)
    objects = models.Manager()
    get_actives = CasaActivesManager()

    def __unicode__(self):
        return "%s CASA" % self.id

    def foto_count(self):
        count = self.fotocasa_set.all().count()
        return count

    def get_precio(self):
        if self.precio == None:
            precio = "A tratar"
        else:
            precio=self.precio
        return precio

    def get_dispo_slug(self):
        if self.disponibilidad==1:
            return 'venta'
        elif self.disponibilidad==2:
            return 'renta'
        else:
            return 'traspaso'

    def get_main_thumb_url(self):
        fotos = self.fotocasa_set.all()

        if fotos.count()>0:
            mains = fotos.filter(principal=True)
            if mains.count() > 0:
                main = mains[0]
            else:
                main = fotos[0]    
            print main.get_thumb_url()
            return main.get_thumb_url()

        else:
            return IMG_NOT_AVAILABLE_CASA

    def get_extra_photo_count(self):
        num_fotos_extra = self.foto_count() - self.paquete.min_fotos
        if num_fotos_extra < 0: 
            num_fotos_extra=0
        return num_fotos_extra

    def has_extra_text(self):
        if len(self.descripcion) > self.paquete.min_texto:
            return True
        else:
            return False
        
    def get_total(self):
        paquete = self.paquete
        p_paquete = paquete.precio
        p_fotosx = self.get_extra_photo_count() * paquete.foto_extra
        if self.has_extra_text():
            p_textox = paquete.texto_extra
        else:
            p_textox = 0
        if self.prioridad:
            p_priori = paquete.prioridad
        else:
            p_priori = 0
        total = p_paquete + p_fotosx + p_textox + p_priori
        return total

    def get_sliced_gallery(self):
        galeria = self.fotocasa_set.all()[:3]
        return galeria

class FotoCasa(models.Model):
    casa=models.ForeignKey(ClasifCasa)
    foto=models.ImageField(upload_to='clasif_casas', max_length=200)
    principal = models.BooleanField()
    

    def save(self):
        if self.principal:
            try:
                temp = FotoCasa.objects.get(principal=True, casa=self.casa)
                if self != temp:
                    temp.principal = False
                    temp.save()
            except FotoCasa.DoesNotExist:
                pass

        super(FotoCasa, self).save()
        if self.foto:
            self.thumb_img(self.foto)
            self.resize_img(self.foto)

    def get_thumb_url(self):
        if self.foto:
            baseurl=self.foto.url
            urlbase, format = baseurl.rsplit('.', 1)
            urlthumb = urlbase + '_T' + '.' +  format
            return urlthumb
        else:
            return "/media/no_disponible.jpeg"

    def resize_img(self, imagen):
        maxw=640
        maxh=640
        method= Image.ANTIALIAS
        w=imagen.width
        h=imagen.height
        path=imagen.path
        if h<=maxh or w<=maxw:
            pass
        else:
            pict= Image.open(path)


            imAspect=float(w)/float(h)
            outAspect=float(maxw)/float(maxh)

            if imAspect>=outAspect:
                img=pict.resize((maxw, int((float(maxw)/imAspect)+0.5)), method)
                img.save(path)
            else:
                img=pict.resize((int((float(maxh)*imAspect)+0.5),maxh),method)
                img.save(path)

    def thumb_img(self, imagen):
        maxw=128
        maxh=128
        method= Image.ANTIALIAS
        w=imagen.width
        h=imagen.height
        path=imagen.path

        pict= Image.open(path)

        nombase, format = path.rsplit('.', 1)

        nomthumb = nombase + '_T' + '.' +  format
	
        imAspect=float(w)/float(h)
        outAspect=float(maxw)/float(maxh)

        if imAspect>=outAspect:
            img=pict.resize((maxw, int((float(maxw)/imAspect)+0.5)), method)
            img.save(nomthumb)
        else:
            img=pict.resize((int((float(maxh)*imAspect)+0.5),maxh),method)
            img.save(nomthumb)


class MarcaAuto(models.Model):
    nombre=models.CharField(max_length=70, unique=True)
    logo = models.ImageField(upload_to="logos_auto", blank=True, null=True)
    fondo = models.ImageField(upload_to="fondos_auto", blank=True, null=True)
    slug = models.SlugField(editable=False, unique=True)
    
    def __unicode__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug= slugify(self.nombre)
        super(MarcaAuto, self).save(*args, **kwargs)

        if self.fondo:
            self.resize_img(self.fondo)
        if self.logo:
            self.resize_logo(self.logo)

    def resize_img(self, imagen):
        maxw=150
        maxh=150
        method= Image.ANTIALIAS
        w=imagen.width
        h=imagen.height
        path=imagen.path
        if h<=maxh or w<=maxw:
            pass
        else:
            pict= Image.open(path)


            imAspect=float(w)/float(h)
            outAspect=float(maxw)/float(maxh)

            if imAspect>=outAspect:
                img=pict.resize((maxw, int((float(maxw)/imAspect)+0.5)), method)
                img.save(path)
            else:
                img=pict.resize((int((float(maxh)*imAspect)+0.5),maxh),method)
                img.save(path)

    def resize_logo(self, imagen):
        maxw=50
        maxh=50
        method= Image.ANTIALIAS
        w=imagen.width
        h=imagen.height
        path=imagen.path
        if h<=maxh or w<=maxw:
            pass
        else:
            pict= Image.open(path)


            imAspect=float(w)/float(h)
            outAspect=float(maxw)/float(maxh)

            if imAspect>=outAspect:
                img=pict.resize((maxw, int((float(maxw)/imAspect)+0.5)), method)
                img.save(path)
            else:
                img=pict.resize((int((float(maxh)*imAspect)+0.5),maxh),method)
                img.save(path)

    def clasif_count(self):
        return self.clasifauto_set.filter(status=0).count()


try:
    admin.site.register(MarcaAuto)
except:
    pass

class ModeloAuto(models.Model):
    marca=models.ForeignKey(MarcaAuto)
    nombre=models.CharField(max_length=70, unique=True)
    slug = models.SlugField(editable=False, unique=True)

    def __unicode__(self):
        return self.nombre
    def save(self, *args, **kwargs):
        self.slug= slugify(self.nombre)
        super(ModeloAuto, self).save(*args, **kwargs)

    def clasif_count(self):
        return self.clasifauto_set.filter(status=0).count()

try:
    admin.site.register(ModeloAuto)
except:
    pass

class SerieAuto(models.Model):
    year = models.IntegerField()
    nombre=models.CharField(max_length=70, unique=True)

    def __unicode__(self):
        return self.nombre

try:
    admin.site.register(SerieAuto)
except:
    pass

class AutoActivesManager(models.Manager):
    def get_query_set(self):
        hoy = datetime.date.today()
        return super(AutoActivesManager, self).get_query_set().filter(status=0, fecha_inicio__lte=hoy, fecha_fin__gte=hoy)


class ClasifAuto(models.Model):
    user = models.ForeignKey(User)
    titulo=models.CharField(max_length=70)
    paquete=models.ForeignKey(Paquete, blank=False, default='')
    precio=models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True, verbose_name="Precio de auto")
    moneda=models.PositiveSmallIntegerField(choices=MONEDA_CHOICES, null=True, blank=True)
    estado=models.ForeignKey(Estado, blank=False, default='')
    municipio=models.ForeignKey(Municipio, blank=False, default='')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    marca=models.ForeignKey(MarcaAuto)
    modelo=models.ForeignKey(ModeloAuto)
    serie=models.ForeignKey(SerieAuto, verbose_name="Año")
    condicion=models.IntegerField(choices=CONDICION_AUTO_CHOICES)
    pasajeros=models.IntegerField(null=True, blank=True) #TODO Estara bien este?
    color=models.CharField(max_length=30)
    transmision=models.PositiveSmallIntegerField(choices=TRANSMISION_CHOICES)
    puertas=models.IntegerField(null=True, blank=True) #TODO Estara bien este?
    cilindros=models.CharField(max_length=16, null=True, blank=True)
    combustible=models.PositiveSmallIntegerField(choices=COMBUST_CHOICES, null=True, blank=True) #TODO Estara bien este?
    kilometraje=models.IntegerField(null=True, blank=True, verbose_name="Kilometraje actual")
    descripcion=models.TextField(null=True, blank=True)
    prioridad = models.BooleanField(help_text="Cargo extra por presencia en pagina principal.")
    usuario_creador = models.ForeignKey(User, related_name="creadorauto_set")
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    fecha_creacion=models.DateField(auto_now_add=True)
    fecha_modificacion=models.DateTimeField(auto_now=True)
    #Informacion de usuario
    #Informacion de usuario
    email=models.EmailField(max_length=75, null=True, blank=True)
    telefono=models.CharField(max_length=30, null=True, blank=True)
    celular=models.CharField(max_length=30, null=True, blank=True)
    direccion=models.TextField(null=True, blank=True)
    objects = models.Manager()
    get_actives = AutoActivesManager()

    def __unicode__(self):
        return "%s AUTO" % self.id

    def foto_count(self):
        count = self.fotoauto_set.all().count()
        return count

    def get_extra_photo_count(self):
        num_fotos_extra = self.foto_count() - self.paquete.min_fotos
        if num_fotos_extra < 0: 
            num_fotos_extra=0
        return num_fotos_extra

    def has_extra_text(self):
        if len(self.descripcion) > self.paquete.min_texto:
            return True
        else:
            return False

    def get_main_thumb_url(self):
        fotos = self.fotoauto_set.all()

        if fotos.count()>0:
            mains = fotos.filter(principal=True)
            if mains.count() > 0:
                main = mains[0]
            else:
                main = fotos[0]    
            print main.get_thumb_url()
            return main.get_thumb_url()

        else:
            return IMG_NOT_AVAILABLE_AUTO

        
    def get_total(self):
        paquete = self.paquete
        p_paquete = paquete.precio
        p_fotosx = self.get_extra_photo_count() * paquete.foto_extra
        if self.has_extra_text():
            p_textox = paquete.texto_extra
        else:
            p_textox = 0
        if self.prioridad:
            p_priori = paquete.prioridad
        else:
            p_priori = 0
        total = p_paquete + p_fotosx + p_textox + p_priori
        return total

    def get_sliced_gallery(self):
        galeria = self.fotoauto_set.all()[:3]
        return galeria


class FotoAuto(models.Model):
    auto=models.ForeignKey(ClasifAuto)
    foto=models.ImageField(upload_to='clasif_autos',max_length=200)
    principal = models.BooleanField()


    def save(self):
        if self.principal:
            try:
                temp = FotoAuto.objects.get(principal=True, auto=self.auto)
                if self != temp:
                    temp.principal = False
                    temp.save()
            except FotoAuto.DoesNotExist:
                pass
        super(FotoAuto, self).save()
        

        if self.foto:
            self.thumb_img(self.foto)
            self.resize_img(self.foto)

    def get_thumb_url(self):
        if self.foto:
            baseurl=self.foto.url
            urlbase, format = baseurl.rsplit('.', 1)
            urlthumb = urlbase + '_T' + '.' +  format
            return urlthumb
        else:
            return "/media/no_disponible.jpeg"

    def resize_img(self, imagen):
        maxw=640
        maxh=640
        method= Image.ANTIALIAS
        w=imagen.width
        h=imagen.height
        path=imagen.path
        if h<=maxh or w<=maxw:
            pass
        else:
            pict= Image.open(path)


            imAspect=float(w)/float(h)
            outAspect=float(maxw)/float(maxh)

            if imAspect>=outAspect:
                img=pict.resize((maxw, int((float(maxw)/imAspect)+0.5)), method)
                img.save(path)
            else:
                img=pict.resize((int((float(maxh)*imAspect)+0.5),maxh),method)
                img.save(path)

    def thumb_img(self, imagen):
        maxw=128
        maxh=128
        method= Image.ANTIALIAS
        w=imagen.width
        h=imagen.height
        path=imagen.path

        pict= Image.open(path)

        nombase, format = path.rsplit('.', 1)

        nomthumb = nombase + '_T' + '.' +  format
	
        imAspect=float(w)/float(h)
        outAspect=float(maxw)/float(maxh)

        if imAspect>=outAspect:
            img=pict.resize((maxw, int((float(maxw)/imAspect)+0.5)), method)
            img.save(nomthumb)
        else:
            img=pict.resize((int((float(maxh)*imAspect)+0.5),maxh),method)
            img.save(nomthumb)

