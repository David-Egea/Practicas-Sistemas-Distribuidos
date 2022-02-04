import pickle
import random
import socket
import time

class Client:
    """ Clase clientes socket en conexiones UDP. En caso de crearse un cliente usando el CMD, se deben facilitar los siguientes argumentos por linea de comandos. 
        Un ejemplo de ejecución es: > python client.py CLIENT_IP CLIENT_PORT CLIENT_ID
        * CLIENT_IP: IP del servidor.
        * CLIENT_PORT: Puerto del servidor.
        * CLIENT_ID: Identificador del cliente
    """

    def __init__(self, id: int = random.randint(0,65536)) -> None:
        # Creaccion del socket
        self._socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
        # Se crea un identificador unico para el cliente
        self._id = id
        
    def __del__(self) -> None:
        # Se cierra el socket
        self._socket.close()

    def send_to_server(self, server_ip: str, server_port, msg: str="Hola soy un cliente") -> None:
        """ Se conecta a la direccion y puerto indiados, y envia un mensaje al servidor. """
        # Creacion del payload on el id del cliente y el mensaje
        client_payload = [self._id,msg]
        # Serializacion del mensaje
        bytes_tx = pickle.dumps(client_payload)
        # Asigna la direccion del servidor
        server_address = (server_ip,server_port)
        # Se muestra la respuesta del servidor
        print(f"[Cliente]:  {msg}")
        contador = 0
        while contador <10:
            try:
                # Envia el mensaje al servidor
                self._socket.sendto(bytes_tx,server_address)
                # Recibe la respuesta del servidor
                bytes_rx = self._socket.recvfrom(1024)
                # Deserializar
                server_payload = pickle.loads(bytes_rx[0])
                # Se muestra la respuesta del servidor
                print(f"[Servidor]: {server_payload[0]}")
            except:
                print("El servidor no se encuentra disponible")
                time.sleep(0.5)
                contador +=1
       
