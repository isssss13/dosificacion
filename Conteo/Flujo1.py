import cv2, numpy as np, mysql.connector, time, os
from threading import Thread

#Se inicializan variables globales
conteo1=0
promedio=0
val1=0
val2=0
idCamara=1
# Definir camara y estacion
status1=True
status2=False
camara1="PruebaMetro.mp4"
estacion="Zaragoza"
hostRemoto="localhost"
# Ajustar el porcentaje
afluencia=100
parametroAlerta=80

def flujo1():
    global conteo1
    global camara1
    cap = cv2.VideoCapture(camara1)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(history=200, nmixtures=10, backgroundRatio=0.2, noiseSigma=0)
    cv2.ocl.setUseOpenCL(False)
    while True:
    	ret, frame = cap.read()
        vid1=cv2.resize(frame,(1266,600),fx=0,fy=0,interpolation = cv2.INTER_CUBIC)
        corte=vid1[290:599, 1:626]
    	if not ret:
    		break
    	fgmask = fgbg.apply(corte)
    	contornosimg = fgmask.copy()
    	(contornos, hierarchy) = cv2.findContours(contornosimg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        conteo1=0
        for c in contornos:
            if cv2.contourArea(c) < 300:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            rectangulo=cv2.rectangle(corte, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if len(rectangulo):
                conteo1+=1
        letrero= 'Objetos: '+ str(conteo1)
        cv2.putText(corte,letrero,(12,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
        # cv2.imshow('original',vid1)
        cv2.imshow('Camara',corte)
    	# cv2.imshow('Umbral',fgmask)
    	# cv2.imshow('Contornos',contornosimg)
    	k = cv2.waitKey(30) & 0xff
    	if k == ord("s"):
    		break
    cap.release()
    cv2.destroyAllWindows()

def conexion():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    while True:
        mycursor = mydb.cursor()
        sql = "INSERT INTO `flujohistorico`(`fecha`, `valores`, `id_camara`) VALUES (now(),%s,%s)"
        val = (conteo1,idCamara)
        mycursor.execute(sql, val)
        mydb.commit()
        # print(mycursor.rowcount, "record inserted.")
        time.sleep(1)

# Promedia los valores recabados y los manda a la base de datos remota donde se encuentra alojado el programa de dosificacion
def algoritmo():
    global promedio
    global afluencia
    mydb = mysql.connector.connect(
        host=hostRemoto,
        user="root",
        passwd="root",
        database="dosificacion"
    )
    while True:
        cam1=valores1()
        cam2=valores2()
        datosR=cam1+cam2
        promedio=((cam1+cam2)*100)/afluencia
        # print(str(promedio)+'%')
        if (promedio>100):
            promedio=100
        mycursor = mydb.cursor()
        sql = "INSERT INTO `dosificacion_historicoafluencia`(`fecha`, `conteo`, `id_estacion_id`) VALUES (now(),%s,(SELECT `id` from `dosificacion_estaciones` WHERE `estacion`=%s))"
        val = (promedio,estacion)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Valor insertado a base remota")
        time.sleep(600)
        
# Cambiar valores de status1 y status2
def valores1():
    global val1
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    if(status1==True):
        mycursor = mydb.cursor()
        mycursor.execute("select sum(`valores`) from flujohistorico where `id_camara`=1")
        myresult = mycursor.fetchone()
        val1=+int(myresult[0])
        limpiar()
        return val1

def valores2():
    global val2
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    if(status2==True):
        mycursor = mydb.cursor()
        mycursor.execute("select sum(`valores`) from flujohistorico where `id_camara`=2")
        myresult = mycursor.fetchall()
        val2=+int(myresult[0])
        return val2
    else:
        return val2

def limpiar():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM `flujohistorico`")
    mydb.commit()

def alerta():
    global promedio
    alerta=0
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    mydb2 = mysql.connector.connect(
        host=hostRemoto,
        user="root",
        passwd="root",
        database="dosificacion"
    )
    while True:
        global parametroAlerta
        mycursor = mydb.cursor()
        mycursor.execute("select `valores` from flujohistorico ORDER BY `id` DESC LIMIT 60")
        myresult = mycursor.fetchall()
        for row in myresult:
            alerta+=int(row[0])
        mydb.commit()
        if(alerta>parametroAlerta):
            mycursor = mydb.cursor()
            sql = "UPDATE alerta SET status = 1,inicio=now()"
            mycursor.execute(sql)
            mydb.commit()            
            print("Alerta activa")
            time.sleep(60)
        else:
            mycursor = mydb.cursor()
            sql = "UPDATE alerta SET status = 0"
            mycursor.execute(sql)
            mydb.commit()
            print("Alerta inactiva")
            time.sleep(10)
            
def conteo():
    if __name__ == "__main__":
        t1 = Thread(target = flujo1)
        t2 = Thread(target = conexion)
        t3 = Thread(target = algoritmo)
        t4 = Thread(target = alerta)
        t1.setDaemon(True)
        t2.setDaemon(True)
        t3.setDaemon(True)
        t4.setDaemon(True)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        while True:
            pass

def comprobacion():
    global idCamara
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="dosificacion_estacion"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select count(*) from alerta")
    myresult = mycursor.fetchone()
    result=int(myresult[0])
    if(result==0):
        mycursor = mydb.cursor()
        sql2 = "INSERT INTO `alerta`(`status`, `inicio`, `id_estacion`) VALUES (0,now(),%s)"
        val = (idCamara,)
        mycursor.execute(sql2, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        print ("Tabla alertas listas para primer uso")
    else:
        print("Tabla alertas OK")

comprobacion()
conteo()