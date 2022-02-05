import socket
import pickle
import time

class Timer:
    @staticmethod
    def get_local_time() -> float:
        return time.time()

""" Servidor Socket UDP """

SERVER_IP = "127.0.0.1"
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
    print(f"[Cliente]: '{client_inst}'")
    if len(c_payload) > 1:
        # Guarda el id del cliente
        client_id = c_payload[1]
    #Se contesta al cliente     
    if client_inst == "EXIT":
        # Se le envia un mesaje estandar al cliente 
        s_payload = "Cerrando servidor..."
        print(f"[Servidor]: '{s_payload}'")
        s_payload = pickle.dumps(s_payload)
        server_socket.sendto(s_payload,client_address)
        break
    else:
        tiempo = time.time()
        s_payload = pickle.dumps(tiempo)
        server_socket.sendto(s_payload,client_address)
        print(f"[Servidor]: '{tiempo}'")

# Al salir de la comunicacion cierra el servidor 
server_socket.close()