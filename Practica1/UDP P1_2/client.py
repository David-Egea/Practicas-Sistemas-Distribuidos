import socket
import pickle

class Client:

    def __init__(self) -> None:
        # Creaccion del socket
        self.socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)

    def __del__(self) -> None:
        # Se cierra el socket
        self.socket.close()

    def send_to_server(self, server_ip: str, msg: str="Hola soy un cliente") -> None:
        # Serializacion del mensaje
        bytes_tx = pickle.dumps(msg)
        #Se pregunta al usuario por el puerto que en el quiere crear el cliente
        ok = False
        while ok!= True:
            # Pregunta al usuario el puerto 
            server_port = input("[Cliente]: Indique el puerto al desea conectarse:\n")
            try:
                server_port = int(input)
                ok = True
            except:
                print(f"[Cliente]: El puerto {server_port} no es valido")
        # Asigna la direccion del servidor
        server_address = (server_ip,server_port)
        # Se muestra la respuesta del servidor
        print(f"[Cliente]: Mensaje enviado al servidor: {bytes_tx}")
        # Envia el mensaje al servidor
        self.socket.sendto(bytes_tx,server_address)
        # Recibe la respuesta del servidor
        bytes_rx = self.socket.recvfrom(1024)
        # Deserializar
        server_response = pickle.loads(bytes_rx)
        # Se muestra la respuesta del servidor
        print(f"[Cliente]: Respuesta del servidor: {server_response}")
