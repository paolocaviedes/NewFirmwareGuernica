import requests
import time

#ip 192.168.29.79

def pausa(sec):
	time.sleep(sec)


#Working
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


"""
print "Ingrese posicion\n"
zoom=(raw_input("Ingrese zoom: "))
pan=(raw_input("Ingrese pan: "))
tilt=(raw_input("Ingrese tilt: "))
print moverCamara("192.168.29.79",1,zoom,pan,tilt)

"""
"""
while zoom>-1:
	zoom=(raw_input("Ingrese zoom: "))
	if zoom!=-1:
		pan=(raw_input("Ingrese pan: "))
		tilt=(raw_input("Ingrese tilt: "))
		print moverCamara(1,zoom,pan,tilt)
"""

"""
#modificar enteros a flotantes
desplazarCamara("192.168.29.79",1,"right",2)
"""

moverCamara("192.168.29.79",1,0,0,0)


actualposition=(0,0,0)

r=int(raw_input("Ingrese caracter para continuar:  "))
while r!=0:
	actualposition=moveCam("192.168.29.79",1,actualposition,"left",350,3)
	r=int(raw_input("Ingrese caracter para continuar:  "))