import socket
import pickle

ip = "127.0.0.1"

#Se pregunta al usuario por el puerto que en el quiere crear el servidor
correcto = False
while correcto!= True:
    puerto_input = input("Indique el puerto en el que desea crear el servidor:\n")
    try:
        puerto = int(puerto_input)
        correcto = True
    except:
        print("Indique un número de puerto correcto")
print("Se comienza a escuchar en la direccion {} y en el puerto {}".format(ip,puerto))
comunicacion = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
comunicacion.bind((ip,puerto))

i = 1
while True:
    #socket.listen()
    #(ip_connected,port_connected) = socket.accept()
    # Se reciben los bytes desde el cliente
    bytes_rx = comunicacion.recvfrom(1024)
    message_recieved = pickle.loads(bytes_rx[0])
    msg = message_recieved[1]
    id = message_recieved[0]

    print("Mensaje: {} desde el cliente {}".format(msg,id))
    print("{} caracteres\n",format(len(msg)))
    print("Desde: {} y puerto {}".format(bytes_rx[1][0],bytes_rx[1][1]))

    #Se contesta al cliente
    msg = ["Hello Client {}".format(id),len(msg)]
    bytes_tx = pickle.dumps(msg)
    comunicacion.sendto(bytes_tx,bytes_rx[1])
    
