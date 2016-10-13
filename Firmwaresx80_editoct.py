import RPi.GPIO as GPIO
import time
import random
from BarradeSensores_lib import centro,delta,ancho,moverCamara

#Configuracion de puertos de recepcion de sennal en placa de la barra de sensores

#Definicion de pines de la GPIO
Sen_1=04
Sen_2=17
Sen_3=27
Sen_4=22
Sen_5=10
Sen_6=09
Sen_7=18

#Declaracion de tipos de pin (entrada o salida)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Sen_1,GPIO.IN)
GPIO.setup(Sen_2,GPIO.IN)
GPIO.setup(Sen_3,GPIO.IN)
GPIO.setup(Sen_4,GPIO.IN)
GPIO.setup(Sen_5,GPIO.IN)
GPIO.setup(Sen_6,GPIO.IN)
GPIO.setup(Sen_7,GPIO.IN)
GPIO.setup(11,GPIO.OUT)


#Definicion de variables estaticas segun sala
anchototal=[min,max]
zoomtotal=[min,max]
ip="192.168.0.1"

#VARIABLE A MODIFICAR SEGUN SALA
tilt=0


#Estructuras de inicializacion automatica

bloquecentro=(anchototal[1]-anchototal[0])/6
bloquezoom=(zoomtotal[1]-zoomtotal[0])/7
estados={"actual":"0000000","pasado":"0000000","antepasado":"0000000"}
cadenaInicial="0000000"
salto=[50,25,12,7,3,0]
posicionactual=(0,0,0)


#Comienzo del ciclo
while(True):

	#Lectura de sennales
	GPIO.output(11,1)
	S1=GPIO.input(Sen_1)
	S2=GPIO.input(Sen_2)
	S3=GPIO.input(Sen_3)
	S4=GPIO.input(Sen_4)
	S5=GPIO.input(Sen_5)
	S6=GPIO.input(Sen_6)
	S7=GPIO.input(Sen_7)

	#Actualizacion de estados 
	estados["antepasado"]=estados["pasado"]
	estados["pasado"]=estados["actual"]
	estados["actual"]=cadenaInicial



	#--------------------main---------------------------------

	delta=delta(estados["pasado"],estados["actual"])
	zoom=ancho(estados["actual"])

	for gap in salto:
		movimiento= gap/100.0 * delta * bloquecentro
		pan=posicionactual[1]+movimiento
		moverCamara(ip,1,zoom,pan,tilt)
		posicionactual=(zoom,pan,tilt)	

	#--------------------end----------------------------------

	#Se hace una pausa
	time.sleep(0.3)
	#Se enciende el led
	GPIO.output(11,0)
	#Se hace otra pausa
	time.sleep(0.2)

	#-------------Actualizacion de cadena----------------------
	#Se lee la sennal de los sensores
	cadena_inicial=str(S7)+str(S6)+str(S5)+str(S4)+str(S3)+str(S2)+str(S1)