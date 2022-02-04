import socket
import pickle
from time import ctime
from datetime import date

SERVER_IP = "192.168.137.171"
SERVER_PORT = 6000

class Timer:
    @ staticmethod
    def get_local_time() -> str:
        return ctime()

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
    print("[Servidor]: El cliente ha enviado la instrucción '{client_inst}'")
    if len(c_payload) > 1:
        # Guarda el id del cliente
        client_id = c_payload[1]
    # En caso de recibir un EXIT se cierra el servidor
    if 'EXIT' in client_inst:
        # Envia un mensaje de adios
        msg = ["Adios",0]
        # Serializa el mensaje
        s_payload = pickle.dumps(msg)
        # se lo envia al cliente
        server_socket.sendto(s_payload,client_address)
        break
    #Se contesta al cliente
    time = getattr(Timer,Timer.get_local_time())
    s_payload = pickle.dumps(time)
    server_socket.sendto(s_payload,client_address)

server_socket.close()