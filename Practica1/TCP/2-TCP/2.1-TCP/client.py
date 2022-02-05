import socket
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
        print(f"[Client]: Disconnected.\n")
        self.socket_client.close()

    def send_instr_to_server(self, instr: str) -> None:
        """ Envia una instruccion al servidor"""
        print(f"[Client]: Sending instruction {instr}")
        # Codifica la instruccion
        tx_bytes = pickle.dumps(instr)
        # Lo envia al servidor
        self.socket_client.sendall(tx_bytes)
        # Recibe la respuesta del servidor
        rx_bytes = self.socket_client.recv(MTU)
        # Decodifica la respuesta
        s_payload = pickle.loads(rx_bytes)
        print(f"[Server]: {s_payload}")