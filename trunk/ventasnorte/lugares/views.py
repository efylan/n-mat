# Create your views here.
from lugares.models import Estado, Municipio
from django.shortcuts import render_to_response, get_object_or_404

def combo_dependiente(request):
	if request.POST:
		estado=request.POST['elegido']
		if not estado=='':
			municipios=Municipio.objects.filter(estado__id=int(estado)).order_by('nombre')
			optionlist=[{'id':'','nombre':"--Elegir Municipio--"}]
			for municipio in municipios:
				optiondict={}
				optiondict['id']=municipio.id
				optiondict['nombre']=municipio.nombre
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

