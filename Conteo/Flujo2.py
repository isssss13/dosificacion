import cv2, numpy as np, mysql.connector, time, os
from threading import Thread

#Se inicializan variables globales
conteo1=0
promedio=0
# Definir camara y estacion
camara1="PruebaMetro.mp4"
idCamara=2
# Ajustar el porcentaje
afluencia=50

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
        print(mycursor.rowcount, "record inserted.")
        time.sleep(10)

def conteo():
    if __name__ == "__main__":
        t1 = Thread(target = flujo1)
        t2 = Thread(target = conexion)
        t1.setDaemon(True)
        t2.setDaemon(True)
        t1.start()
        t2.start()
        while True:
            pass

conteo()