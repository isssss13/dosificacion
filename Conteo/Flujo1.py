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
        corte=vid1[363:599, 1:626]
    	# Si hemos llegado al final del video salimos
    	if not ret:
    		break
    	# Aplicamos el algoritmo
    	fgmask = fgbg.apply(corte)
    	# Copiamos el umbral para detectar los contornos
    	contornosimg = fgmask.copy()
    	# Buscamos contorno en la imagen
    	(contornos, hierarchy) = cv2.findContours(contornosimg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    	# Se reinicia la variable conteo para validar los datos actuales
        conteo1=0
        # Recorremos todos los contornos encontrados
        for c in contornos:
            # Eliminamos los contornos mas pequenos
            if cv2.contourArea(c) < 500:
                continue
            # Obtenemos el bounds del contorno, el rectangulo mayor que engloba al contorno
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectangulo del bounds
            rectangulo=cv2.rectangle(corte, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if len(rectangulo):
                conteo1+=1
        #5.Poner texto en imagen
        letrero= 'Objetos: '+ str(conteo1)
        cv2.putText(corte,letrero,(7,5),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
        cv2.imshow('original',vid1)
        cv2.imshow('Camara',corte)
    	# cv2.imshow('Umbral',fgmask)
    	# cv2.imshow('Contornos',contornosimg)
    	# Sentencias para salir, pulsa 's' y sale
    	k = cv2.waitKey(30) & 0xff
    	if k == ord("s"):
    		break
    # Liberamos la camara y cerramos todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

# Conexion a la base de datos dependiendo la camara cambia la variable idCamara
def conexion():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    while True:
        mycursor = mydb.cursor()
        sql = "INSERT INTO `historico`(`fecha`, `valores`, `id_camara`) VALUES (now(),%s,%s)"
        val = (conteo1,idCamara)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        time.sleep(10)

# Promedia los valores recabados y los manda a la base de datos remota donde se encuentra alojado el programa de dosificacion
def algoritmo():
    global promedio
    global afluencia
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion"
    )
    while True:
        cam1=valores1()
        cam2=valores2()
        datosR=cam1+cam2
        if(afluencia<datosR):
            afluencia=datosR
        elif(afluencia>datosR):
            if(afluencia<100):
                afluencia=100
            else:
                afluencia=(afluencia+datosR)/2
        promedio=((cam1+cam2)*100)/afluencia
        print(promedio)
        # mycursor = mydb.cursor()
        # sql = "INSERT INTO `dosificacion_historicoafluencia`(`fecha`, `conteo`, `id_estacion_id`) VALUES (now(),%s,%s)"
        # val = (promedio,estacion)
        # mycursor.execute(sql, val)
        # mydb.commit()
        # print(mycursor.rowcount, "Valor insertado a base remota")
        time.sleep(10)
        
# Realiza la busqueda en la base de datos para calcular el porcentaje de los datos recabados por las camaras
# Cambiar valores de status1 y status2
def valores1():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    if(status1==1):
        mycursor = mydb.cursor()
        mycursor.execute("select `valores` from historico where `id_camara`=1 order by id DESC limit 1")
        myresult = mycursor.fetchone()
        val1=int(myresult[0])
        return val1
def valores2():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    if(status2==1):
        global val2
        mycursor = mydb.cursor()
        mycursor.execute("select `valores` from historico where `id_camara`=2 order by id DESC limit 1")
        myresult = mycursor.fetchone()
        val2=int(myresult[0])
        return val2
    else:
        return val2

def conteo():
    if __name__ == "__main__":
        t1 = Thread(target = flujo1)
        t2 = Thread(target = conexion)
        t3 = Thread(target = algoritmo)        
        t1.setDaemon(True)
        t2.setDaemon(True)
        t3.setDaemon(True)
        t1.start()
        t2.start()
        t3.start()
        while True:
            pass

conteo()