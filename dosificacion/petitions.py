from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as do_login,logout as do_logout

from .models import estaciones

def iniciarSesion(request):
    if request.user.is_authenticated:
        return redirect('/')    
    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.method == "POST":
        user = authenticate(username=username, password=password)
        if user is not None:
            do_login(request, user)
            return JsonResponse({'resultado':"success",'text':"Datos Correctos"})
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