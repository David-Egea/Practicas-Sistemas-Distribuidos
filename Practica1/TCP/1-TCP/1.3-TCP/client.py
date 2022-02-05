from difflib import diff_bytes
import socket
import time
import pickle

# Se define el tamaño de MTU
MTU = 1024 # En bytes 

class Client:
    """ Clase Cliente TCP """

    def __init__(self, server_address: tuple = ("localhost",6780)) -> None:
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(server_address)

    def __del__(self) -> None:
        # Se cierra el socket del cliente
        # print(f"[Client]: Disconnected.\n")
        self.socket_client.close()

    def send_msg_to_server(self, msg: str = "Hi TCP Server") -> None:
        """ Envia el mensaje indicado al servidor"""
        print(f"[Client]: {msg}")
        payload = pickle.dumps(msg)
        self.socket_client.sendall(payload)
        # Decodifica los datos recibidos por paquetes
        p = 0 # Contador de paquetes
        while True:
            p = p + 1 # Incrementa el contador
            rx_bytes = self.socket_client.recv(MTU)
            server_payload = pickle.loads(rx_bytes)
            print(f"[Server]: {server_payload} (Packet {p})")
            if len(server_payload) is not MTU:
                break
        print(f"[Server]: {server_payload} (Full msg)")

    def get_server_time(self) -> float:
        """ Solicita al servidor TCP la hora. Devuelve la diferencia"""
        # Recoge la hora actual en el cliente
        client_time = time.time()
        c_payload = "get_time"
        tx_bytes = pickle.dumps(c_payload)
        # Envia la peticion al servidor
        self.socket_client.sendall(tx_bytes)
        # Decodifica el timepo del servidor recibido
        rx_bytes = self.socket_client.recv(MTU)
        s_payload = pickle.loads(rx_bytes)
        server_time = float(s_payload)
        # print(f"[Server]: {server_time}")
        # Se calcula la diferencia
        diff_time = server_time - client_time
        # print(f"[Client]: Elapsed time was {server_time} (s)")
        return diff_time