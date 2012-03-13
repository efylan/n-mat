# coding: latin1
from django import forms
from clasificados.models import ClasifCasa, ClasifAuto, ModeloAuto
from django.contrib.auth.models import User

TIPO_BUSQUEDA_CHOICES=((1, 'Autos'),(2, 'Casas e Inmuebles'))


class CrearCasaForm(forms.ModelForm):
    userid=forms.IntegerField(label="ID de usuario")
    class Meta:
        model=ClasifCasa
        fields=('userid','titulo','paquete','precio','moneda', 'categoria_casa', 'disponibilidad','estado', 'municipio', 'domicilio', 'colonia', 'codigo_postal', 'referencia', 'condicion', 'pisos', 'superficie', 'recamaras', 'banos','descripcion', 'prioridad')
    
    def __init__(self, *args, **kwargs):
        super(CrearCasaForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            casa = self.instance
            self.fields['userid'].initial=casa.user.id
        self.fields['userid'].widget.attrs['class']='required'
        self.fields['titulo'].widget.attrs['class']='required'
        self.fields['disponibilidad'].widget.attrs['class']='required'
        self.fields['condicion'].widget.attrs['class']='required'
        self.fields['pisos'].widget.attrs['class']='required'

class CrearAutoForm(forms.ModelForm):
    userid=forms.IntegerField(label="ID de usuario")
    class Meta:
        model=ClasifAuto
        fields=('userid', 'titulo', 'paquete', 'precio', 'moneda', 'estado', 'municipio', 'marca', 'modelo', 'serie', 'condicion', 'pasajeros', 'color', 'transmision', 'puertas', 'cilindros', 'combustible', 'kilometraje', 'descripcion', 'prioridad')

    def __init__(self, *args, **kwargs):
        super(CrearAutoForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            auto = self.instance
            self.fields['userid'].initial=auto.user.id

        self.fields['userid'].widget.attrs['class']='required'
        self.fields['titulo'].widget.attrs['class']='required'
        self.fields['marca'].widget.attrs['class']='required'
        self.fields['modelo'].widget.attrs['class']='required'
        self.fields['serie'].widget.attrs['class']='required'
        self.fields['condicion'].widget.attrs['class']='required'
        self.fields['color'].widget.attrs['class']='required'
        self.fields['transmision'].widget.attrs['class']='required'
        if self.is_bound:
            self.fields['modelo'].queryset=ModeloAuto.objects.all()
        else:
            self.fields['modelo'].queryset=ModeloAuto.objects.none()

class DisplayUserForm(forms.Form):
    username = forms.CharField(max_length=30, label="Nombre de Usuario")
    first_name = forms.CharField(max_length=30, label="Nombre", required=False)
    last_name = forms.CharField(max_length=30, label="Apellidos", required=False)
    email = forms.EmailField(max_length=75,label="Correo electronico", required=False)
    phone_number = forms.CharField(max_length=30, required=False,label = 'Telefono Fijo')
    cellphone = forms.CharField(max_length=30, required=False,label = 'Celular')
    address = forms.CharField(widget=forms.Textarea, label='Direccion', required=False)

    def __init__(self, casa=None, *args, **kwargs):
        super(DisplayUserForm, self).__init__(*args, **kwargs)

        if casa:
            self.fields['username'].initial=casa.user.username
            self.fields['first_name'].initial = casa.user.first_name
            self.fields['last_name'].initial = casa.user.last_name
            self.fields['email'].initial = casa.email
            self.fields['phone_number'].initial = casa.telefono
            self.fields['cellphone'].initial = casa.celular
            self.fields['address'].initial = casa.direccion
            self.fields['username'].widget.attrs['class']='readonly found'
            self.fields['first_name'].widget.attrs['class']='readonly'
            self.fields['last_name'].widget.attrs['class']='readonly'
            self.fields['username'].widget.attrs['readonly']=True
            self.fields['first_name'].widget.attrs['readonly']=True
            self.fields['last_name'].widget.attrs['readonly']=True

class PhotoForm(forms.Form):
    def __init__(self, anuncio, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        foto_count = anuncio.foto_count()
        num_fotos = anuncio.paquete.min_fotos - foto_count
        if num_fotos < 0:
            num_fotos=0

        precio = anuncio.paquete.foto_extra


        for foto in range(num_fotos):
            if foto == 0:
                if foto_count>0:
                    self.fields['picture'+str(foto+1)] = forms.ImageField(label = "Foto "+str(foto+1), required=False)
                else:
                    self.fields['main_picture'] = forms.ImageField(label = "Foto Principal", required=False)
            else:
                self.fields['picture'+str(foto+1)] = forms.ImageField(label = "Foto "+str(foto+1), required=False)


        for extra in range(5):
            self.fields['extra'+str(extra+1)] = forms.ImageField(label = "Extra "+str(extra+1)+" ($%s pesos)" % precio, required=False)
            self.fields['extra'+str(extra+1)].widget.attrs['class'] = 'red'

class IdForm(forms.Form):
    search_id = forms.IntegerField()
    tipo = forms.ChoiceField(choices=TIPO_BUSQUEDA_CHOICES)

class NameSearchForm(forms.Form):
    id_user = forms.IntegerField(required=False, label="ID de usuario")
    username = forms.CharField(required=False, label="Username")
    name = forms.CharField(required=False, label="Nombre")
    last_name = forms.CharField(required=False, label="Apellido")
