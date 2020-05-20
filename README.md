**Sistema de flujo de personas**
Se requiere Numpy, CV2 y mysql.connector

El principal es Flujo1.py si se maneja una sola camara para el conteo
Si activa la segunda camara se debe de correr Flujo2.py

Flujo1.py cuenta con las variables necesarias al principio del codigo con la finalidad de modificarlas dependiendo de los servicios que se activaran

*****************************************************************
status1: Siempre debe ser true para realizar el porcentaje de la estacion
status2: Por defecto esta en False,cuando se agrege una segunda camara se debe cambiar a True
camara1: IP de la camara que contara el flujo de usuarios
estacion: Nombre de la estacion de instalacion, es Obligatorio que presente el mismo nombre que se encuentra en el sistema web
hostRemoto: IP del servidor web donde se encuentra alojada la base de datos utilizada por el sistema web
*****************************************************************