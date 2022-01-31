import socket

class Client:

    def __init__(self) -> None:
        # Creaccion del socket
        self.socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)

    def __del__(self) -> None:
        # Se cierra el socket
        socket.close()

    def send_to_server(self, server_ip: str, server_port: int, msg: str="Hello im a client") -> None:
        # Serializacion del mensaje
        bytes_tx = str.encode(msg)
        # Se muestra la respuesta del servidor
        print(f"[Cliente]: Mensaje enviado al servidor: {bytes_tx}")
        # Asigna la direccion del servidor
        server_address = (server_ip,server_port)
        # Envia el mensaje al servidor
        self.socket.sendto(bytes_tx,server_address)
        # Recibe la respuesta del servidor
        bytes_rx = self.socket.recvfrom(1024)
        # Se muestra la respuesta del servidor
        print(f"[Cliente]: Respuesta del servidor: {bytes_rx}")
