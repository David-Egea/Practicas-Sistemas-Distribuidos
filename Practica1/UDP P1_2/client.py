import socket
import pickle

class Client:

    def __init__(self) -> None:
        # Creaccion del socket
        self.socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)

    def __del__(self) -> None:
        # Se cierra el socket
        self.socket.close()

    def send_to_server(self, server_ip: str, server_port,msg: str="Hola soy un cliente") -> None:
        # Serializacion del mensaje
        bytes_tx = pickle.dumps(msg)
        
        # Asigna la direccion del servidor
        server_address = (server_ip,server_port)
        # Se muestra la respuesta del servidor
        print(f"[Cliente]: Mensaje enviado al servidor: {msg}")
        # Envia el mensaje al servidor
        self.socket.sendto(bytes_tx,server_address)
        # Recibe la respuesta del servidor
        bytes_rx = self.socket.recvfrom(1024)
        # Deserializar
        server_response = pickle.loads(bytes_rx)
        # Se muestra la respuesta del servidor
        print(f"[Cliente]: Respuesta del servidor: {server_response}")
