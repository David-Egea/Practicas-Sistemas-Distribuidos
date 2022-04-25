import socket
import cv2
import pickle

class Client:
    """ Clase Cliente TCP """
    
    def __init__(self) -> None:
        self.server_address = ("localhost",6000) # TODO
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(self.server_address)

    # def __del__(self) -> None:
        # # Se cierra el socket del cliente
        # self.socket_client.close()

    def client_handler(self) -> None:
        global print_lock
        while True:
            
            """ Waits for the message from the server"""
            data = pickle.loads(self.socket_client.recv(1024))
            self.processData(data)
            # Data is sended back to the server
            self.socket
        self.socket_client.close() # TODO
    def process_data(self,data):
        # TODO
        
