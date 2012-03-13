# coding: latin1
from django import forms
from clasificados.models import CategoriaCasa, MarcaAuto, ModeloAuto, SerieAuto, CONDICION_AUTO_CHOICES
from lugares.models import Estado, Municipio
DISPO_CHOICES = (('', '---------'),(1, 'Venta'),(2, 'Renta'),(3, 'Traspaso'))
CONDICION_CASA_CHOICES = (('', '---------'), (1, 'Excelente'),(2,'Buena'),(3,'Regular'))
CONDICION_AUTO_CHOICES = (('', '---------'), (1, 'Excelente'),(2,'Buena'),(3,'Regular'), (4,'Chocado'), )
TRANSMISION_CHOICES = (('', '---------'),(1,'Standard'),(2,'Automatico'))


class CasaSimpleSearchForm(forms.Form):
    disponibilidad = forms.ChoiceField(choices=DISPO_CHOICES, required=False)
    categoria = forms.ModelChoiceField(CategoriaCasa.objects.all(), required=False, label="Categoría")
    estado = forms.ModelChoiceField(Estado.objects.all(), required=False)
    municipio = forms.ModelChoiceField(Municipio.objects.all(), required=False)
    condicion = forms.ChoiceField(CONDICION_CASA_CHOICES, required=False, label="Condición")

    def __init__(self, *args, **kwargs):
        super(CasaSimpleSearchForm, self).__init__(*args, **kwargs)

        if self.is_bound:
            self.fields['municipio'].queryset=Municipio.objects.all()
        else:
            self.fields['municipio'].queryset=Municipio.objects.none()


class CasaAdvSearchForm(forms.Form):
    disponibilidad = forms.ChoiceField(choices=DISPO_CHOICES, required=False)
    categoria_casa = forms.ModelChoiceField(CategoriaCasa.objects.all(), required=False)
    estado = forms.ModelChoiceField(Estado.objects.all(), required=False)
    municipio = forms.ModelChoiceField(Municipio.objects.all(), required=False)
    colonia = forms.CharField(required=False)
    condicion = forms.ChoiceField(CONDICION_CASA_CHOICES, required=False)
    pisos = forms.IntegerField(required=False)
    recamaras = forms.IntegerField(required=False)
    banos = forms.IntegerField(required=False)


class AutoSimpleSearchForm(forms.Form):
    marca = forms.ModelChoiceField(MarcaAuto.objects.all(), required=False)
    modelo = forms.ModelChoiceField(ModeloAuto.objects.all(), required=False)
    serie = forms.ModelChoiceField(SerieAuto.objects.all(), required=False)
    transmision = forms.ChoiceField(choices=TRANSMISION_CHOICES, required=False)
    estado = forms.ModelChoiceField(Estado.objects.all(), required=False)
    municipio = forms.ModelChoiceField(Municipio.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(AutoSimpleSearchForm, self).__init__(*args, **kwargs)

        if self.is_bound:
            self.fields['modelo'].queryset=ModeloAuto.objects.all()
            self.fields['municipio'].queryset=Municipio.objects.all()
        else:
            self.fields['modelo'].queryset=ModeloAuto.objects.none()
            self.fields['municipio'].queryset=Municipio.objects.none()



"""
class AutoAdvSearchForm(forms.Form)
    marca = forms.ModelChoiceField(MarcaAuto, required=False)
    modelo = forms.ModelChoiceField(ModeloAuto, required=False)
    serie = forms.ModelChoiceField(SerieAuto, required=False)
    transmision = forms.ChoiceField(choices=TRANSMISION_CHOICES, required=False)
    estado = forms.ModelChoiceField(Estado.objects.all(), required=False)
    municipio = forms.ModelChoiceField(Municipio.objects.all(), required=False)
    condicion = forms.ChoiceField(choices=CONDICION_AUTO_CHOICES, required=False)
    pasajeros = forms.IntegerField(required=False)
    puertas = forms.IntegerField(required=False)
    cilindros = forms.IntegerField(required=False) #TODO cambiar a choice?
    combustible = forms.ChoiceField(choices=COMBUST_CHOICES, required=False)
    kilometraje = forms.IntegerField(label = "Kilometraje menor a", required=False)
"""
