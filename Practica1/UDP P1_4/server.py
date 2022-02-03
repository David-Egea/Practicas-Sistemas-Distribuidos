import socket
import pickle
from sys import argv

ip = argv[1]
puerto = int(argv[2])

print("Se comienza a escuchar en la direccion {} y en el puerto {}".format(ip,puerto))
comunication = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
comunication.bind((ip,puerto))

i = 1
while True:
    #socket.listen()
    #(ip_connected,port_connected) = socket.accept()
    # Se reciben los bytes desde el cliente
    bytes_rx = comunication.recvfrom(1024)
    message_recieved = pickle.loads(bytes_rx[0])
    msg = message_recieved[1]
    id = message_recieved[0]

    if 'EXIT' in msg:
        msg = ["Adios",0]
        bytes_tx = pickle.dumps(msg)
        comunication.sendto(bytes_tx,bytes_rx[1])

        break
    print("Mensaje: {} desde el cliente {}".format(msg,id))
    print("{} caracteres\n".format(len(msg)))
    print("Desde: {} y puerto {}".format(bytes_rx[1][0],bytes_rx[1][1]))

    #Se contesta al cliente
    msg = ["Hello Client {}".format(id),len(msg)]
    bytes_tx = pickle.dumps(msg)
    comunication.sendto(bytes_tx,bytes_rx[1])

comunication.close()
