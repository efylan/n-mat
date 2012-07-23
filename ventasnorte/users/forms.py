# coding: latin1
from django import forms
from django.contrib.auth.models import User
from clasificados.models import ClasifCasa, ClasifAuto

class LoginForm(forms.Form):
    username=forms.CharField(label="Nombre de Usuario")
    password=forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='required'
        self.fields['password'].widget.attrs['class']='required'


class PasswordResetForm(forms.Form):
    username=forms.CharField(label="Nombre de Usuario")

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='required'


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=3, help_text="Nombre de usuario entre 3 y 30 caracteres", widget=forms.TextInput(attrs={ 'class': 'required' }), error_messages={'invalid': "El nombre de usuario debe tener entre 3 y 30 caracteres."}, label="Nombre de usuario")

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={ 'class': 'required' }), label="Nombre(s)")

    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={ 'class': 'required' }), label="Apellidos")

    email = forms.EmailField(max_length=75,label="Correo electronico", help_text="Ingresar un e-mail valido.")
    phone_number = forms.CharField(max_length=30, required=False,label = 'Telefono Fijo')
    cellphone = forms.CharField(max_length=30, required=False,label = 'Celular')
    address = forms.CharField(widget=forms.Textarea, label='Direccion')


    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("El nombre de usuario que usted ingreso ya esta ocupado")

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("Un usuario con este correo ya se encuentra registrado")
        return self.cleaned_data['email']

class PasswordChangeForm(forms.Form):
    password = forms.CharField(max_length=30, help_text="Ingresar su contraseña actual.", 
        widget=forms.PasswordInput(attrs={ 'class': 'required' }),
        error_messages={'invalid': "La contraseña debe contener almenos 5 caracteres."}, label="Contraseña")

    new_password = forms.CharField(max_length=30, min_length=5, help_text="Su nueva contraseña debe contener almenos 6 caracteres",label="Nueva Contraseña" ,
        widget=forms.PasswordInput(attrs={ 'class': 'required' }),
        error_messages={'invalid': "El password debe contener almenos 5 caracteres."})

    new_password2 = forms.CharField(max_length=30, help_text="Favor de volver a ingresar su password", 
        widget=forms.PasswordInput(attrs={ 'class': 'required' }),label="Confirmar Nueva Contraseña")

    def clean(self):
        error=''
        bandera=0
        if 'new_password' in self.cleaned_data and 'new_password2' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['new_password2']:
                error = error + "*Los passwords suministrados no coinciden."
                bandera=1

        if bandera==1:
            raise forms.ValidationError(error)

        return self.cleaned_data




class CrearCasaForm(forms.ModelForm):
    class Meta:
        model=ClasifCasa
        fields=('titulo','paquete','precio','moneda', 'categoria_casa', 'disponibilidad','estado', 'municipio', 'domicilio', 'colonia', 'codigo_postal', 'referencia', 'condicion', 'pisos', 'superficie', 'recamaras', 'banos','descripcion', 'prioridad')
    
    def __init__(self, *args, **kwargs):
        super(CrearCasaForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            casa = self.instance

        self.fields['titulo'].widget.attrs['class']='required'
        self.fields['disponibilidad'].widget.attrs['class']='required'
        self.fields['condicion'].widget.attrs['class']='required'
        self.fields['pisos'].widget.attrs['class']='required'

class CrearAutoForm(forms.ModelForm):
    class Meta:
        model=ClasifAuto
        fields=('titulo', 'paquete', 'precio', 'moneda', 'estado', 'municipio', 'marca', 'modelo', 'serie', 'condicion', 'pasajeros', 'color', 'transmision', 'puertas', 'cilindros', 'combustible', 'kilometraje', 'descripcion', 'prioridad')

    def __init__(self, *args, **kwargs):
        super(CrearAutoForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            auto = self.instance

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

    def __init__(self, user=None, *args, **kwargs):
        super(DisplayUserForm, self).__init__(*args, **kwargs)

        if user:
            perfil = user.get_profile()
            self.fields['username'].initial=user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone_number'].initial = perfil.telefono
            self.fields['cellphone'].initial = perfil.celular
            self.fields['address'].initial = perfil.direccion
            self.fields['username'].widget.attrs['class']='readonly found'
            self.fields['first_name'].widget.attrs['class']='readonly'
            self.fields['last_name'].widget.attrs['class']='readonly'
            self.fields['username'].widget.attrs['readonly']=True
            self.fields['first_name'].widget.attrs['readonly']=True
            self.fields['last_name'].widget.attrs['readonly']=True

