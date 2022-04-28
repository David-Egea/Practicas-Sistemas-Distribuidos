import socket
import cv2
import pickle
import threading

class SlaveNode:
    """ Clase Cliente TCP """
    
    def __init__(self) -> None:
        self.server_address = ("localhost",6000) # TODO Change ip address
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(self.server_address)
        self.buffer_size = 4096
        # If the connection is succecfull, the thread starts
        thread = threading.Thread(target = self.client_handler())
        thread.start()
        #Waiting for the thread to finish
        thread.join()
        print("Client finished")

    def client_handler(self) -> None:
        global print_lock
        while True:
            """ Waits for the message from the server"""
            data = pickle.loads(self.recieve_data())
            print("Data recieved")

            data_processed = self.process_data(data)
            # Data is sended back to the server
            payload = pickle.dumps(data_processed)
            self.socket_client.sendall(payload)

            #Sending the confirmation message
            msg = "Ok"
            payload = pickle.dumps(data_processed)
            self.socket_client.sendall(payload)

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
        self.socket_client.setblocking(True)
        data = bytearray()
        try:
            while True:
                data+= bytearray(self.socket_client.recv(self.buffer_size))
                # A partir de ahora si no hay datos que leer finalizamos el bucle
                self.socket_client.setblocking(False)
        except socket.error:
            self.socket_client.setblocking(True)
            return data

        

if __name__ == "__main__":
    client = Client()