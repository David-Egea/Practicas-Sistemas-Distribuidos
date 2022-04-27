import socket
import cv2
import pickle
import threading
from configuration import Configuration
import time
import io

class Client:
    """ Clase Cliente TCP """
    
    def __init__(self) -> None:
        self.configuration = Configuration()
        self.ip_address = self.configuration.get_config_param("network","ip")
        self.port = int(self.configuration.get_config_param("network","port"))
        self.buffer_size = int(self.configuration.get_config_param("comms","buffer_size"))

        self.server_address = (self.ip_address,self.port) 
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(self.server_address)
        
        # If the connection is succecfull, the thread starts
        thread = threading.Thread(target = self.client_handler)
        thread.start()
        #Waiting for the thread to finish
        thread.join()
        print("Client finished")

    def client_handler(self) -> None:
        global print_lock
        while True:
            """ Waits for the message from the server"""
            data = self.recieve_data()
            print(data)

            data_processed = self.process_data(data)
            print("Data processed")
            # Data is sended back to the server
            
            self.sendData(data_processed)
            print("Data sended")
            time.sleep(0.1)
            #Sending the confirmation message
            msg = "Ok"
            
            self.sendData(msg)

            print("Confirmation sended")
            #Waiting confirmation
            msg = self.recieve_data()
            print("Data recieved")
            if msg == 'EXIT':
                self.socket_client.close()
                break
            elif msg =='Ok':
                pass
    def process_data(self,data):
        return_data = []
        for image in data:
            return_data.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        return 	return_data

    def recieve_data(self):
        try:
            n_bytes = b""
            byte = None
            while byte != b"\r":
                
                byte = self.socket_client.recv(1)
                
                n_bytes += byte

            n_bytes = int(n_bytes)
            buffer = io.BytesIO()
            recibidos = 0
            print(n_bytes)
            while recibidos < n_bytes:
                msg = self.socket_client.recv(self.buffer_size)
                buffer.write(msg)
                recibidos += len(msg)
            buffer.seek(0)
            data = pickle.loads(buffer.read())
            
        except:
            print("Error")
        time.sleep(0.1)
        return data
    def sendData(self,data):
    
        payload = pickle.dumps(data)
        n_bytes = self.socket_client.send(str(len(payload)).encode() + b"\r")
        self.socket_client.sendall(payload) 
        

        """
        self.socket_client.setblocking(True)
        data = bytearray()
        try:
            while True:
                data+= bytearray(self.socket_client.recv(self.buffer_size))
                # A partir de ahora si no hay datos que leer finalizamos el bucle
                self.socket_client.setblocking(False)
        except socket.error:
            self.socket_client.setblocking(True)
            time.sleep(0.1)
            return data
        """
        

if __name__ == "__main__":
    client = Client()