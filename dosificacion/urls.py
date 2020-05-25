from django.urls import path

from . import views

app_name='dosificacion'
urlpatterns = [
    path('', views.index, name='index'),
    path('addusuarios', views.createUser),
    path('passupd', views.changePass),
    path('editusuarios', views.editUser),
    path('lineas', views.lineas, name='estaciones'),
    path('updLineas', views.uptLineas, name='actLineas'),
    path('addEstacion', views.addEstacion, name='addEstacion'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('login', views.login, name='login'),
    path('initsesion', views.iniciarSesion),
    path('logout', views.logout,name='logout'),
    path('graficas/<str:nameestacion>', views.graficasEstacion,name='graficas'),
]