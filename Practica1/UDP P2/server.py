import socket
import pickle

#Se pregunta al usuario por el puerto que en el quiere crear el servidor
correcto = False
while correcto!= True:
    puerto_input = input("Indique el puerto en el que desea crear el servidor:\n")
    try:
        puerto = int(puerto_input)
        correcto = True
    except:
        print("Indique un número de puerto correcto")

socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
socket.bind(("127.0.0.1",puerto))

i = 1
while True:
    # Se reciben los bytes desde el cliente
    bytes_rx = socket.recvfrom(1024)
    message_recieve = pickle.loads(bytes_rx)
    message = bytes_rx[0]
    address = bytes_rx[1]
    print("Mensaje: {}".format(message))
    print("Desde: {}".format(address))

    #Se contesta al cliente
    msg = "Hello Client {}".format(i)
    bytes_tx = pickle.dumps(msg)
    socket.sendto(bytes_tx,address)
    i +=1