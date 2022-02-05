import socket

# Se define el tamaño de MTU
MTU = 20 # En bytes 

class Client:
    """ Clase Cliente TCP """

    def __init__(self, server_address: tuple = ("localhost",6780)) -> None:
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(server_address)

    def __del__(self) -> None:
        # Se cierra el socket del cliente
        print(f"[Client]: Disconnected.\n")
        self.socket_client.close()

    def send_msg_to_server(self, msg: str = "Hi TCP Server") -> None:
        """ Envia el mensaje indicado al servidor"""
        print(f"[Client]: {msg}")
        self.socket_client.sendall(msg.encode())
        # Decodifica los datos recibidos por paquetes
        p = 0 # Contador de paquetes
        while True:
            p = p + 1 # Incrementa el contador
            data = self.socket_client.recv(MTU).decode()
            print(f"[Server]: {data} (Packet {p})")
            if len(data) is not MTU:
                break
        print(f"[Server]: {data} (Full msg)")