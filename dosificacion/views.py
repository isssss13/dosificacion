from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import linea,estaciones,HistoricoAfluencia,Trenes
from .petitions import iniciarSesion,logout,changePass,editUser,createUser,addEstacion,desactivarUsuario,restablecerPassword

datos=linea.objects.order_by('id')# pylint: disable=no-member
estacion=estaciones.objects.order_by('id')# pylint: disable=no-member
listLineas=linea.objects.order_by('id')# pylint: disable=no-member


def usuarios(request):
    listUsuarios=User.objects.all()
    context={
        'nombre':'Administrar Usuarios',
        'datos':datos,
        'estaciones':estacion,
        'listaUsuarios':listUsuarios
    }
    return render(request,'pages/usuarios.html',context)

def login(request):
    return render(request,'registration/login.html')

@login_required(login_url='/login')
def index(request):
    createUser(request)
    context={
        'nombre':'Principal- Dosificacion',
        'datos':datos,
        'estaciones':estacion,
    }
    return render(request,'plantilla.html',context)

@login_required(login_url='/login')
def lineas(request):
    if request.user.is_staff:
        actestacion=estaciones.objects.order_by('id')# pylint: disable=no-member
        context={
                'nombre':'Administrar lineas',
                'datos':datos,
                'estaciones':actestacion,
                'lineas':listLineas,
        }
        return render(request,'pages/lineas.html',context)

@login_required(login_url='/login')
def graficasEstacion(request,nameestacion):
    datosestacion=estaciones.objects.get(estacion=nameestacion)# pylint: disable=no-member
    grafica=HistoricoAfluencia.objects.all().filter(id_estacion=datosestacion.id).order_by('-id')[:12]# pylint: disable=no-member
    fechaa=[
        grafica[0].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[1].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[2].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[3].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[4].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[5].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[6].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[7].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[8].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[9].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[10].fecha.strftime('%Y-%m-%d %H:%M'),
        grafica[11].fecha.strftime('%Y-%m-%d %H:%M'),
    ]
    graf=[
        grafica[0].conteo,
        grafica[1].conteo,
        grafica[2].conteo,
        grafica[3].conteo,
        grafica[4].conteo,
        grafica[5].conteo,
        grafica[6].conteo,
        grafica[7].conteo,
        grafica[8].conteo,
        grafica[9].conteo,
        grafica[10].conteo,
        grafica[11].conteo,
    ]
    context={    
        'fechaaxis1':fechaa[0],
        'fechaaxis2':fechaa[1],
        'fechaaxis3':fechaa[2],
        'fechaaxis4':fechaa[3],
        'fechaaxis5':fechaa[4],
        'fechaaxis6':fechaa[5],
        'fechaaxis7':fechaa[6],
        'fechaaxis8':fechaa[7],
        'fechaaxis9':fechaa[8],
        'fechaaxis10':fechaa[9],
        'fechaaxis11':fechaa[10],
        'fechaaxis12':fechaa[11],
        'data1':graf[0],
        'data2':graf[1],
        'data3':graf[2],
        'data4':graf[3],
        'data5':graf[4],
        'data6':graf[5],
        'data7':graf[6],
        'data8':graf[7],
        'data9':graf[8],
        'data10':graf[9],
        'data11':graf[10],
        'data12':graf[11],
        'nombre':'Estadisticas '+datosestacion.estacion,
        'datos':datos,
        'estaciones':estacion,
    }
    
    return render(request,'pages/graficas.html',context)    

@login_required(login_url='/login')
def uptLineas(request):
    if request.user.is_staff:
        statusSistema=request.POST['status']
        idEstacion=request.POST['id_Estacion']
        if request.method== 'POST':
            estacion=estaciones.objects.get(pk=idEstacion)# pylint: disable=no-member
            estacion.statusSistema=statusSistema
            estacion.save()
            return HttpResponseRedirect(reverse('dosificacion:estaciones'))
        else:
            return HttpResponseRedirect(reverse('dosificacion:estaciones'))
