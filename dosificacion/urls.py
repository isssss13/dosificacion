from django.urls import path

from . import views

app_name='dosificacion'
urlpatterns = [
    path('', views.index, name='index'),
    # path('administrador', views.administracion, name='administrador'),
    path('lineas', views.lineas, name='estaciones'),
    path('updLineas', views.uptLineas, name='actLineas'),
    path('login', views.login, name='login'),
    path('logout', views.logout,name='logout'),
    path('graficas/<int:idEstacion>', views.graficasEstacion,name='graficas'),
]