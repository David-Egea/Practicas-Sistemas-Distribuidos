import socket
import pickle
from time import ctime
from datetime import date

class Timer:
    @staticmethod
    def get_local_time() -> str:
        return ctime()

""" Servidor Socket UDP """

SERVER_IP = "192.168.43.214"
SERVER_PORT = 6000

# Se crea el socket server
server_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
# Se fija el puerto a la direccion 
server_socket.bind((SERVER_IP,SERVER_PORT))


while True:
    print("[Servidor]: Esperando conexión del cliente... ")
    # Recibe los datos enviados por un cliente
    data,client_address = server_socket.recvfrom(1024)
    print(f"[Servidor]: Se ha conectado un cliente con IP: {SERVER_IP} y PORT: {SERVER_PORT}")
    # mensaje descodificado
    c_payload = pickle.loads(data)
    # Guarda la instruccion
    client_inst = c_payload[0]
    print("[Cliente]: '{client_inst}'")
    if len(c_payload) > 1:
        # Guarda el id del cliente
        client_id = c_payload[1]
    #Se contesta al cliente
    if client_inst == "_get_local_time":
        time = Timer.get_local_time()
        s_payload = pickle.dumps(time)
        server_socket.sendto(s_payload,client_address)
    elif client_inst == "EXIT":
        # Se cierra el servidor
        break
    else:
        # Se le envia un mesaje estandar al cliente 
        s_payload = pickle.dumps("Hola cliente")
        server_socket.sendto(s_payload,client_address)
        print("[Servidor]: '{client_inst}'")

server_socket.close()