from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import logout as do_logout,authenticate,login as do_login
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import linea,estaciones,HistoricoAfluencia,Trenes

def logout(request):
    do_logout(request)
    return redirect('/login')
userlog=0
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

# vistas para actualiza y editar 

@login_required(login_url='/login')
def addEstacion(request):
    if request.user.is_staff:
        linea=request.POST['lineaAdd']
        nombre=request.POST['nombreEstacionAdd']
        status=request.POST['statusAdd']
        if request.method== 'POST':
            estacion=estaciones(estacion=nombre,statusSistema=status,id_linea_id=linea)
            estacion.save()
            return HttpResponseRedirect(reverse('dosificacion:estaciones'))
        else:
            return HttpResponseRedirect(reverse('dosificacion:estaciones'))

@login_required(login_url='/login')
def createUser(request):
    if request.user.is_staff:
        nickname=request.POST.get('nickname')
        correo=request.POST.get('correo')
        passw='12345'
        staff=request.POST.get('permisos')
        if request.method == "POST":
            try:
                user=User.objects.create_user(nickname,correo,passw)
                if staff=='1':
                    user.is_staff=True
                    user.save()
                    return JsonResponse({'resultado':"success",'text':"Usuario administrador creado correctamente"})
                else:
                    user.save()
                    return JsonResponse({'resultado':"success",'text':"Usuario creado correctamente"})
            except:
                return JsonResponse({'resultado':"error",'text':"Error al crear usuario"})

@login_required(login_url='/login')
def editUser(request):
    id=request.POST.get('usuario_E')
    nombre=request.POST.get('nombre_E')
    apellidos=request.POST.get('app_E')
    correo=request.POST.get('correo_E')
    staff=request.POST.get('permisos_E')
    if request.method == "POST":
        try:
            user=User.objects.get(pk=id)
            user.first_name=nombre
            user.last_name=apellidos
            user.email=correo
            if staff=='1':
                user.is_staff=True
            else:
                user.is_staff=False
            user.save()
            return JsonResponse({'resultado':"success",'text':"Datos actualizados correctamente"})
        except:
            return JsonResponse({'resultado':"error",'text':"Error al actualizar"})

@login_required(login_url='/login')
def changePass(request):
    usuario=request.POST.get('username')
    passnew=request.POST.get('pass')
    if request.method == "POST":
        try:
            user=User.objects.get(username=usuario)
            user.set_password(passnew)
            user.save()
            return JsonResponse({'resultado':"success",'text':"Contraseña cambiada por favor inicie sesion nuevamente"})
        except:
            return JsonResponse({'resultado':"error",'text':"Error al actualizar"})