import pickle
import random
import socket
from time import sleep

WAIT_TIME = 10

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
        # Asigna la direccion del servidor
        server_address = (server_ip,server_port)
        # Creacion del payload on el id del cliente y el mensaje
        client_payload = [self._id,msg]
        # Serializacion del mensaje
        bytes_tx = pickle.dumps(client_payload)
        # Se muestra el mensaje enviado al servidor
        print(f"[Cliente]:  {msg}")
        # Comprueba que el servidor este encendido
        for seg in range(1,WAIT_TIME+1):
            try:
                # Envia el mensaje al servidor
                self._socket.sendto(bytes_tx,server_address)
                # Recibe la respuesta del servidor
                bytes_rx = self._socket.recvfrom(1024)
                break
            except ConnectionResetError:
                if seg == WAIT_TIME:
                    # Si se ha cumplido el tiempo maximo
                    print(f"[Cliente]:  Ha expirado el tiempo de espera del servidor ({seg} s).")
                    print(f"[Cliente]:  Se ha abortado la comunicación ({seg} s).")
                    return
                else:
                    # El servidor esta apagado
                    print(f"[Cliente]:  El servidor está apagado ({seg} s).")
                    # Espera un segundo
                    sleep(1)
        # Deserializar
        server_payload = pickle.loads(bytes_rx[0])
        # Se muestra la respuesta del servidor
        print(f"[Servidor]: {server_payload[0]}")
