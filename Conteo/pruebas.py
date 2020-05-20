import cv2, numpy as np, mysql.connector, time, os
from threading import Thread

#Se inicializan variables globales
conteo1=0
promedio=0
status1=1
status2=1
val1=0
val2=0
# Definir camara y estacion
camara1="PruebaMetro.mp4"
estacion=2
idCamara=1
# Ajustar el porcentaje
afluencia=50

def flujo1():
    global conteo1
    global camara1
    # Capturamos el video
    cap = cv2.VideoCapture(camara1)
    
    
    # Llamada al metodo
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history=200, nmixtures=10, backgroundRatio=0.2, noiseSigma=0)
    # Deshabilitamos OpenCL, si no hacemos esto no funciona
    cv2.ocl.setUseOpenCL(False)
    while True:
    	# Leemos el siguiente frame
    	ret, frame = cap.read()
        vid1=cv2.resize(frame,(1266,600),fx=0,fy=0,interpolation = cv2.INTER_CUBIC)
        corte=vid1[392:599, 4:720]
    	if not ret:
    		break
    	fgmask = fgbg.apply(corte)
    	contornosimg = fgmask.copy()
    	# Buscamos contorno en la imagen
    	(contornos, hierarchy) = cv2.findContours(contornosimg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    	# Se reinicia la variable conteo para validar los datos actuales
        conteo1=0
        # Recorremos todos los contornos encontrados
        # Se redimenciona las pantallas 
        
    	# Mostramos las capturas
        cv2.imshow('Camara',vid1)
        cv2.imshow('Camara2',corte)
    	k = cv2.waitKey(30) & 0xff
    	if k == ord("s"):
    		break
    # Liberamos la camara y cerramos todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

def conteo():
    if __name__ == "__main__":
        t1 = Thread(target = flujo1)
        t1.setDaemon(True)
        t1.start()
        while True:
            pass

conteo()