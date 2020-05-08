from django import forms

# from .models import estaciones

class profile(forms.Form):
    Area = forms.CharField(label='Area', max_length=50)


# class EstacionesForm(forms.Form):
#     class Meta:
#         model =estaciones
#         fields =[
#             'id',
#             'estacion',
#             'statusSistema',
#         ]
#         labels={
#             'id':'Nombre',
#             'estacion':'Nombre Estacion',
#             'statusSistema':'Estatus del sistema',
#         }
#         widgets={
#             'id':forms.HiddenInput(attrs={'name':'id_Estacion','id':'idEstacion'}),
#             'estacion':forms.TextInput(attrs={'name':"nombreEstacion",'id':"nombreEstacion",'required':True}),
#         }