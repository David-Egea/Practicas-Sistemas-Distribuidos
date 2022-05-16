import socket
from typing import Any
import cv2
import pickle
from configuration import Configuration
import time
import io
from job import Job
import random
import os
from threading import Thread
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# TODO: CHECK THE PATH BEFORE EXPORTING TO DOCKER
# -----------------------------------------------
import pathlib

FILE_PATH = f"{pathlib.Path(__file__).parent.resolve()}"
# -----------------------------------------------

class Client:
    """ TCP Client class """
    
    def __init__(self) -> None:
        # Initial configuration
        self.configuration = Configuration(f"{os.path.join(FILE_PATH,'client_config.ini')}")
        self.ip_address_server = self.configuration.get_config_param("network","ip_server")
        self.port_server = int(self.configuration.get_config_param("network","port_server"))
        self.buffer_size = int(self.configuration.get_config_param("comms","buffer_size"))
        self.id = random.randint(1,1000)
        self.job_type = "process.image.color_to_gray"
        self.ftp_user = self.configuration.get_config_param("ftp","username")
        self.ftp_password = self.configuration.get_config_param("ftp","password")
        self.ftp_directory = os.path.join(FILE_PATH,self.configuration.get_config_param("ftp","ftpDirectory"))
        self.ftp_port = int(self.configuration.get_config_param("ftp","port"))
        # Sets the Ip address
        self.ip = socket.gethostbyname(socket.gethostname())
        # Creating the ftp server thread
        Thread(target = self.ftp_server).start()
        # Variables to load data and save it
        self.directoryToDo = os.path.join(FILE_PATH,self.configuration.get_config_param("client","directoryToDo"))
        self.directoryToSave = os.path.join(FILE_PATH,self.configuration.get_config_param("client","directoryToSave"))
        self.indexImage = 0
        # Elements to process on each job
        self.elements_load = int(self.configuration.get_config_param("client","elementsLoad"))
        # Creating the connection with the server
        self.server_address = (self.ip_address_server,self.port_server) 
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(self.server_address)
        self.main()
        # Waiting for the thread to finish
        print("Client finished")

    def send_job(self) -> None:
       """ Function to create a new job"""
       if self.check_missing_payload:
        # Loading data
        payload = self.load_payload()
        if len(payload)>0 and not any(elem is None for elem in payload):
            # Building the job object
            job = Job(self.id,self.job_type,payload)
            # Sending data
            self.send_data(job)
        else:
            raise Exception("There is no element to load")

    def check_missing_payload(self)->bool:
        """Function if there is payload to process"""
        listed_directory = os.listdir(self.directoryToDo)
        if len(listed_directory)>0:
            return True
        else:
            return False
    
    def load_payload(self)->list:
        """Function to load all the payload to process"""
        print("Loading payload")
        listed_directory = os.listdir(self.directoryToDo)
        payload_process = []
        i  = 0
        for element in listed_directory:
            if i< self.elements_load:
                try:
                    image= cv2.imread(self.directoryToDo+"\\"+element)
                    i=i+1
                    payload_process.append(image)
                    # Constructs the path pof the element
                    element_path = os.path.join(self.directoryToDo,element)
                    # The element is deleted
                    os.remove(element_path)
                except:
                    break
            else:
                break
        print("Payload loaded {} elements".format(len(payload_process)))
        return payload_process

    def save_payload(self, payload: Any) -> None:
        """ Function to save the results of the processing"""
        for element in payload:
            # Writing the image
            cv2.imwrite(self.directoryToSave+str(self.indexImage)+".jpg",element)
            # Incrementing the index by one
            self.indexImage += 1

    def recieve_data(self) -> Any:
        """ Receives the data sent from server. The data is fragmented to meet the MTU buffer max size."""
        data = []
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
        except ConnectionError:
            print("Error")
        time.sleep(0.1)
        return data

    def send_data(self, data: Any):
        """ Sends a data throught the client socket."""
        payload = pickle.dumps(data)
        self.socket_client.send(str(len(payload)).encode() + b"\r")
        self.socket_client.sendall(payload)
    
    def ftp_server(self):
        """ Starts a connection between FTP server and client. The """
        authorizer = DummyAuthorizer()
        authorizer.add_user(self.ftp_user, self.ftp_password, self.ftp_directory, perm='elradfmwMT')
        handler = FTPHandler
        handler.authorizer = authorizer
        handler.banner = 'FTP Server is ready.'
        handler.passive_ports = range(60000, 65535)
        print("Ip: {}".format(self.ip))
        address = (self.ip,self.ftp_port)
        server = FTPServer(address, handler)
        server.max_cons = 256
        server.max_cons_per_ip = 5
        print("FTP server mounted.")
        server.serve_forever()

    def main(self):
        """Main thread for the application"""
        while True:
            if self.check_missing_payload():
                # Sending the job
                try:
                    self.send_job()
                except:
                    break

                # Waits for the job to arrive
                msg  = ""
                while True:
                    msg = self.recieve_data()
                    if msg == "Ok":
                        break
                    self.save_payload(msg.payload)
                    conf_msg = "Ok"
                    self.send_data(conf_msg)
        print("While finished")
                    

if __name__ == "__main__":
    try:
        client = Client()
    except KeyboardInterrupt:
        print("Client finished")
    