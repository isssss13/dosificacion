from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as do_login,logout as do_logout

from .models import estaciones,HistoricoAfluencia

def iniciarSesion(request):
    if request.user.is_authenticated:
        return redirect('/')    
    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.method == "POST":
        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            return JsonResponse({'resultado':"success",'text':"Error en los datos"})
        else:
            return JsonResponse({'resultado':"error",'text':"Error en los datos"})

def logout(request):
    do_logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def changePass(request):
    usuario=request.POST.get('usuario_pass_E')
    passnew=request.POST.get('password')
    if request.method == "POST":
        try:
            user=User.objects.get(pk=usuario)
            user.set_password(passnew)
            user.save()
            return JsonResponse({'resultado':"success",'text':"Contraseña cambiada por favor inicie sesion nuevamente"})
        except:
            return JsonResponse({'resultado':"error",'text':"Error al actualizar"})

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

def desactivarUsuario(request):
    username = request.POST.get('admin')
    usuario = request.POST.get('usuario')
    delUser=User.objects.get(username=usuario)
    password = request.POST.get('passConf')
    if request.method == "POST":
        user = authenticate(username=username, password=password)
        if user is not None:
            delUser.is_active=0
            delUser.save()
            return JsonResponse({'resultado':"success",'text':"Usuario eliminado"})
        else:
            return JsonResponse({'resultado':"error",'text':"Error en los datos"})

def restablecerPassword(request):
    username = request.POST.get('admin_P')
    password = request.POST.get('passConf_P')
    passReset = request.POST.get('usuario_P')
    passUser=User.objects.get(username=passReset)
    if request.method == "POST":
        user = authenticate(username=username, password=password)
        if user is not None:
            passUser.set_password("12345")
            passUser.save()
            return JsonResponse({'resultado':"success",'text':"La contraseña se reestablecio con exito"})
        else:
            return JsonResponse({'resultado':"error",'text':"Error en la contraseña"})

def cambiarPermisos(request):
    usuario=request.POST.get('usuario_Permisos')
    permisos=request.POST.get('permisos_Usuario')
    changeUser=User.objects.get(username=usuario)
    if request.method == "POST":
        try:
            if permisos=='0':
                changeUser.is_staff=1
                changeUser.is_superuser=1
            elif permisos=='1':
                changeUser.is_staff=1
                changeUser.is_superuser=0
            else:
                changeUser.is_staff=0
                changeUser.is_superuser=0
            changeUser.save()
            return JsonResponse({'resultado':"success",'text':"Usuario actualizado"})
        except:
            return JsonResponse({'resultado':"error",'text':"Error en la actualizacion"})
    
def graficas(request):
    estacion= request.POST.get('dato')
    grafica=HistoricoAfluencia.objects.all().filter(id_estacion=estacion).order_by('-id')[:12]
    try:
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
    
        return JsonResponse({'resultado':"success",'text':"datos en camino","fec":fechaa,"graf":graf})
    except:
        return JsonResponse({'resultado':"error",'text':"Sin datos de la estacion por el momento"})