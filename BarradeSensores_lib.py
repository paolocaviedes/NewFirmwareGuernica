import requests
import time

#Se define una pausa
def pausa(sec):
	time.sleep(sec)


#Funcion que al recibir la cadena, entrega la cantidad de ceros antes del primer 1 pero de atras hacia adelante
def contarZeros(cadena):
	countZero=0
	flag=True
	for elemento in cadena:
		if flag:
			if elemento=='0':
				countZero+=1
			else:
				flag=False
	return countZero

#Funcion que al recibir la cadena, entrega la cantidad de ceros antes del primer 1 pero de atras hacia adelante
def contarZerosReverse(cadena):
	cadena=cadena[::-1]
	countZero=0
	flag=True
	for elemento in cadena:
		if flag:
			if elemento=='0':
				countZero+=1
			else:
				flag=False
	return countZero

#funcion que entrega cuantos caracteres hay entre el primer y ultimo 1 de la cadena
def contarOnes(cadena):
	if contarZeros(cadena)==7:
		return 0
	return 7 - (contarZeros(cadena)+contarZerosReverse(cadena))

#Funcion que entrega la cadena en el formato correcto, sin ceros entre el primer y ultimo 1
def transformarCadena(cadena):
	cadenaDefinitiva=''
	if contarZeros(cadena)==7:
		return '0000000'
	elif contarZeros(cadena)==0 and contarZerosReverse==0:
		return '1111111'
	else:
		cadenaDefinitiva='0'*contarZeros(cadena)+'1'*contarOnes(cadena)+'0'*contarZerosReverse(cadena)
		return cadenaDefinitiva

#Funcion que retorna el centro de la cadena, segun los sensores activos
def centro(cadena):
	center=contarZeros(cadena)+(contarOnes(cadena)/2.0)
	return center

#Funcion que retorna el ancho de la cadena, segun los sensores activos
def ancho(cadena):
	ancho=contarOnes(cadena)
	return ancho

#Funcion que determina la diferencia entre la posicion pasada y la actual
def delta(cadenapasada,cadenaactual):
	absolutepast=abs(centro(cadenapasada))
	absolutepresent=abs(centro(cadenaactual))
	delta=absolutepresent-absolutepast
	return delta


#Funciones para el movimiento de la camara

#Funcion moverCamara, al ingresar la ip, el id de la camara y un zoom,pan y tilt, la camara se moverá automaticamente a dicha posicion. 
def moverCamara(ip,Idcam,zoom,pan,tilt):

	url = "http://"+str(ip)+"/putxml"

	payload = "<Command>\r\n<Camera>\r\n<PositionSet command=\"True\">\r\n<CameraId>"+str(Idcam)+"</CameraId>\r\n<Zoom>"+str(zoom)+"</Zoom>\r\n<Pan>"+str(pan)+"</Pan>\r\n<Tilt>"+str(tilt)+"</Tilt>\r\n</PositionSet>\r\n</Camera>\r\n</Command>"
	headers = {
	    'content-type': "text/xml",
	    'authorization': "Basic YWRtaW46MTIzNDU=",
	    'cache-control': "no-cache",
	    'postman-token': "6a4759eb-ccfc-8f79-c828-770e0b326486"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)

	return(response.text)


#Funcion que a partir de una direccion y un tiempo se moverá durante dicho tiempo en la direccion indicada
#Working unidad minima 1sec.
def desplazarCamara(ip,Idcam,direccion,tiempo):
	flagpan=False
	flagtilt=False

	comando=direccion.lower().capitalize()
	print comando

	if comando=="Left" or comando=="Right":
		leftright=comando
		updown=""
		flagpan=True
	elif comando=="Up" or comando=="Down":
		updown=comando
		leftright=""
		flagtilt=True

	url = "http://"+str(ip)+"/putxml"

	if flagpan:			
		for i in range(tiempo):
			payload = "<Command>\r\n<Camera>\r\n<Ramp command=\"True\">\r\n<CameraId>"+str(Idcam)+"</CameraId>\r\n<Pan>"+str(leftright)+"</Pan>\r\n</Ramp>\r\n</Camera>\r\n</Command>"
				
			headers = {
					'content-type': "text/xml",
					'authorization': "Basic YWRtaW46MTIzNDU=",
					'cache-control': "no-cache",
					'postman-token': "6a4759eb-ccfc-8f79-c828-770e0b326486"
					}

			response = requests.request("POST", url, data=payload, headers=headers)
					
			print (response.text)
			#pausa(0.1)

		#detener movimiento

		url = "http://"+str(ip)+"/putxml"
		payload = "<Command>\r\n<Camera>\r\n<Ramp command=\"True\">\r\n<CameraId>"+str(Idcam)+"</CameraId>\r\n<Pan>Stop</Pan>\r\n</Ramp>\r\n</Camera>\r\n</Command>"
				
		headers = {
				'content-type': "text/xml",
				'authorization': "Basic YWRtaW46MTIzNDU=",
				'cache-control': "no-cache",
				'postman-token': "6a4759eb-ccfc-8f79-c828-770e0b326486"
				}

		response = requests.request("POST", url, data=payload, headers=headers)
		print (response.text)

	if flagtilt:
		for i in range(tiempo):
			payload = "<Command>\r\n<Camera>\r\n<Ramp command=\"True\">\r\n<CameraId>"+str(Idcam)+"</CameraId>\r\n<Tilt>"+str(updown)+"</Tilt>\r\n</Ramp>\r\n</Camera>\r\n</Command>"
				
			headers = {
					'content-type': "text/xml",
					'authorization': "Basic YWRtaW46MTIzNDU=",
					'cache-control': "no-cache",
					'postman-token': "6a4759eb-ccfc-8f79-c828-770e0b326486"
					}

			response = requests.request("POST", url, data=payload, headers=headers)
					
			print (response.text)
			#pausa(0.1)

		#detener movimiento

		url = "http://"+str(ip)+"/putxml"
		payload = "<Command>\r\n<Camera>\r\n<Ramp command=\"True\">\r\n<CameraId>"+str(Idcam)+"</CameraId>\r\n<Tilt>Stop</Tilt>\r\n</Ramp>\r\n</Camera>\r\n</Command>"
				
		headers = {
				'content-type': "text/xml",
				'authorization': "Basic YWRtaW46MTIzNDU=",
				'cache-control': "no-cache",
				'postman-token': "6a4759eb-ccfc-8f79-c828-770e0b326486"
				}

		response = requests.request("POST", url, data=payload, headers=headers)
		print (response.text)

	return "OK"

#Funcion que a partir de la posicion actual, una direccion, la cantidad de movimiento y un tiempo determinado, la camara se moverá hacia tal direccion, la cantidad indicada durante el tiempo indicado.
#actualpos=(zoom,pan,tilt)
#pos= int que indica cuanto se requiere mover
def moveCam(ip,Idcam,actualpos,direction,pos,tiempo):
	diferencia=int(pos/tiempo)
	#print diferencia
	salto=0

	direction=direction.lower()

	for i in range(tiempo):
		if direction=="up":
			move=actualpos[2]+diferencia
			moverCamara(ip,Idcam,actualpos[0],actualpos[1],move)
			actualposition=(actualpos[0],actualpos[1],actualpos[2]+pos)
		elif direction=="down":
			move=actualpos[2]+salto+diferencia
			#print move
			moverCamara(ip,Idcam,actualpos[0],actualpos[1],move)
			actualposition=(actualpos[0],actualpos[1],actualpos[2]+pos)
		elif direction=="left":
			move=actualpos[1]+diferencia+salto
			#print move
			moverCamara(ip,Idcam,actualpos[0],move,actualpos[2])
			#print "bien"
			actualposition=(actualpos[0],actualpos[1]+pos,actualpos[2])
		elif direction=="right":
			move=actualpos[1]+diferencia
			moverCamara(ip,Idcam,actualpos[0],move,actualpos[2])			
			actualposition=(actualpos[0],actualpos[1]+pos,actualpos[2])

		salto+=diferencia
		#time.sleep(0.0001)
	return actualposition