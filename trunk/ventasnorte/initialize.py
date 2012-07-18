import os
from ventasnorte.clasificados.models import Paquete, CategoriaCasa, MarcaAuto, ModeloAuto
from django.template.defaultfilters import slugify


#----PAQUETES-----------------------------------

paquetes = [{'nombre':'Gratis', 'precio':0, 'dias_activo':7, 'min_fotos':0, 'min_texto':100, 'foto_extra':5, 'texto_extra':5,'prioridad':15},
            {'nombre':'Basico', 'precio':9, 'dias_activo':15, 'min_fotos':1, 'min_texto':140, 'foto_extra':5, 'texto_extra':5,'prioridad':15},
            {'nombre':'Extendido', 'precio':15, 'dias_activo':15, 'min_fotos':2, 'min_texto':250, 'foto_extra':5, 'texto_extra':5,'prioridad':15},
            {'nombre':'Premium', 'precio':21, 'dias_activo':30, 'min_fotos':5, 'min_texto':500, 'foto_extra':5, 'texto_extra':5,'prioridad':15},
           ]
print "Comienza inicializacion de paquetes..."
for paquete in paquetes:
    paq = Paquete()
    paq.nombre = paquete['nombre']
    paq.precio = paquete['precio']
    paq.dias_activo = paquete['dias_activo']
    paq.min_fotos = paquete['min_fotos']
    paq.min_texto = paquete['min_texto']
    paq.foto_extra = paquete['foto_extra']
    paq.texto_extra = paquete['texto_extra']
    paq.prioridad = paquete['prioridad']
    try:
        paq.save()
        print paq.nombre, "...OK"
    except:
        print paq.nombre, "... DUPLICADO O ERROR"

    
#----CATEGORIA CASA-----------------------------

#categorias = ['Casa','Departamento','Terreno','Local','Bodega','Otro',]
[]
for cate in categorias:
    cat = CategoriaCasa()
    cat.nombre = cate
    cat.slug = slugify(cate)
    try:
        cat.save()
        print cat.nombre, "...OK"
    except:
        print cat.nombre, "... DUPLICADO O ERROR"


#----MARCA AUTO---------------------------------

marcas = open(os.path.join(os.path.dirname(__file__), 'make.csv'),'r')
for line in marcas.readlines():
    decoded = line.split(",")
    marca = MarcaAuto()
    marca.id = decoded[0]
    marca.nombre = decoded[1]
    marca.slug = slugify(decoded[1]) 
#    try:
    marca.save()
    print marca.nombre, "...OK"
#    except:
#        print marca.nombre, "... DUPLICADO O ERROR"

#----MODELO AUTO--------------------------------

modelos = open( os.path.join(os.path.dirname(__file__), 'models.csv'),'r')
for line in modelos.readlines():
    decoded = line.split(",")
    modelo = ModeloAuto()
    modelo.marca_id = decoded[0]
    modelo.nombre = decoded[1] 
    marca.slug = slugify(decoded[1])
#    try:
    modelo.save()
    print modelo.nombre, "...OK"
#    except:
#        print modelo.nombre, "... DUPLICADO O ERROR"

#----USUARIOS-----------------------------------


