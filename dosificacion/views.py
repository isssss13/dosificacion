from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import logout as do_logout,authenticate,login as do_login
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

from .models import linea,estaciones,HistoricoAfluencia,Trenes

def logout(request):
    do_logout(request)
    return redirect('/login')

def login(request):
    # Creamos el formulario de autenticación vacío
    if request.user.is_authenticated:
        return redirect('/')
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "registration/login.html", {'form': form})

datos=linea.objects.order_by('id')# pylint: disable=no-member
estacion=estaciones.objects.order_by('id')# pylint: disable=no-member
listLineas=linea.objects.order_by('id')# pylint: disable=no-member

def index(request):
    createUser(request)
    if request.user.is_authenticated:
        context={
            'nombre':'Principal- Dosificacion',
            'datos':datos,
            'estaciones':estacion,
        }
        return render(request,'plantilla.html',context)
    return redirect('/login')


# def administracion(request):    
#     estacion=estaciones.objects.order_by('id')# pylint: disable=no-member
#     datos=linea.objects.order_by('id')# pylint: disable=no-member
#     context={
#         'nombre':'Administrar usuarios',
#         'estaciones':estacion,
#         'datos':datos,
#     }
#     if request.user.is_authenticated:        
#         return render(request,'pages/usuarios.html',context)
#     return redirect('/login')


def lineas(request):
    createUser(request)
    actestacion=estaciones.objects.order_by('id')# pylint: disable=no-member
    context={
            'nombre':'Administrar lineas',
            'datos':datos,
            'estaciones':actestacion,
            'lineas':listLineas,
    }
    if request.user.is_authenticated:
        return render(request,'pages/lineas.html',context)
    return redirect('/login')




def graficasEstacion(request,nameestacion):
    createUser(request)
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
    if request.user.is_authenticated:
        return render(request,'pages/graficas.html',context)
    return redirect('/login')
    
    # datos=linea.objects.order_by('id')# pylint: disable=no-member
    # grafica=HistoricoAfluencia.objects.all().filter(id_estacion=idname).order_by('-id')[:12]# pylint: disable=no-member
    # trenes=Trenes.objects.filter(id_estacion=idEstacion).order_by('-id')# pylint: disable=no-member
    # fechaTren=[
    #     trenes[0].fecha,
    #     trenes[1].fecha,
    #     trenes[2].fecha,
    #     trenes[3].fecha,
    #     trenes[4].fecha,
    #     trenes[5].fecha,
    #     trenes[6].fecha,
    # ]

    # grafTren=[
    #     trenes[0].conteoTrenes,
    #     trenes[1].conteoTrenes,
    #     trenes[2].conteoTrenes,
    #     trenes[3].conteoTrenes,
    #     trenes[4].conteoTrenes,
    #     trenes[5].conteoTrenes,
    #     trenes[6].conteoTrenes,
    # ]
    
    



    # context
    #     'fechaaxis1':fechaa[0],
    #     'fechaaxis2':fechaa[1],
    #     'fechaaxis3':fechaa[2],
    #     'fechaaxis4':fechaa[3],
    #     'fechaaxis5':fechaa[4],
    #     'fechaaxis6':fechaa[5],
    #     'fechaaxis7':fechaa[6],
    #     'fechaaxis8':fechaa[7],
    #     'fechaaxis9':fechaa[8],
    #     'fechaaxis10':fechaa[9],
    #     'fechaaxis11':fechaa[10],
    #     'fechaaxis12':fechaa[11],
    #     'data1':graf[0],
    #     'data2':graf[1],
    #     'data3':graf[2],
    #     'data4':graf[3],
    #     'data5':graf[4],
    #     'data6':graf[5],
    #     'data7':graf[6],
    #     'data8':graf[7],
    #     'data9':graf[8],
    #     'data10':graf[9],
    #     'data11':graf[10],
    #     'data12':graf[11],

        # 'fechaTren1':fechaTren[0],
        # 'fechaTren2':fechaTren[1],
        # 'fechaTren3':fechaTren[2],
        # 'fechaTren4':fechaTren[3],
        # 'fechaTren5':fechaTren[4],
        # 'fechaTren6':fechaTren[5],
        # 'fechaTren7':fechaTren[6],

        # 'grafTren1':grafTren[0],
        # 'grafTren2':grafTren[1],
        # 'grafTren3':grafTren[2],
        # 'grafTren4':grafTren[3],
        # 'grafTren5':grafTren[4],
        # 'grafTren6':grafTren[5],
        # 'grafTren7':grafTren[6],
        # 'nombre':'Estadisticas '+estacion.estacion,
        # 'ipcamara1':estacion.ip_camara1,
        # 'ipcamara2':estacion.ip_camara2,

        # 'datos':datos,
        # 'estaciones':estacioness,
        # 'estacion':estacion,

def uptLineas(request):
    if request.user.is_authenticated:
        statusSistema=request.POST['status']
        idEstacion=request.POST['id_Estacion']
        if request.method== 'POST':
            estacion=estaciones.objects.get(pk=idEstacion)# pylint: disable=no-member
            estacion.statusSistema=statusSistema
            estacion.save()
            messages.success(request, 'Estacion actualizada correctamente!')
            return HttpResponseRedirect(reverse('dosificacion:estaciones'))
        else:
            messages.error(request, 'Error al actualizar!')
            return HttpResponseRedirect(reverse('dosificacion:estaciones'))
    return redirect('/login')


def addEstacion(request):
    linea=request.POST['lineaAdd']
    nombre=request.POST['nombreEstacionAdd']
    status=request.POST['statusAdd']
    if request.method== 'POST':
        estacion=estaciones(estacion=nombre,statusSistema=status,id_linea_id=linea)
        estacion.save()
        messages.success(request, 'Estacion agregada correctamente!')
        return HttpResponseRedirect(reverse('dosificacion:estaciones'))
    else:
        messages.error(request, 'Error al crear estacion!')
        return HttpResponseRedirect(reverse('dosificacion:estaciones'))

# def delEstacion(request,idEstacion):
#     estacion=estaciones.objects.get(pk=idEstacion)# pylint: disable=no-member

def createUser(request):
    nickname=request.POST.get('nickname')
    correo='ivan.mcr.swami@gmail-com'
    passw='12345'    
    if request.method == "POST":
        try:
            user=User.objects.create_user(nickname,correo,passw)
            user.save()
            return JsonResponse({'resultado':"success",'text':"Usuario creado correctamente"})
        except:
            return JsonResponse({'resultado':"error",'text':"Error al crear usuario"})
    # form = UserCreationForm()
    # if request.method == "POST":
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Usuario creado correctamente')
    #     else:
    #         messages.error(request, 'Error al crear el usuario')