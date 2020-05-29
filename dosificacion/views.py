from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from .models import linea,estaciones,HistoricoAfluencia,Trenes
from .petitions import iniciarSesion,logout,changePass,editUser,createUser,addEstacion,desactivarUsuario,restablecerPassword,cambiarPermisos,graficas

datos=linea.objects.order_by('id')# pylint: disable=no-member
estacion=estaciones.objects.order_by('id')# pylint: disable=no-member
listLineas=linea.objects.order_by('id')# pylint: disable=no-member

@login_required(login_url='/login')
@staff_member_required(login_url='/')
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
@staff_member_required(login_url='/')
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
    context={    
        'id':datosestacion.id,
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
