import socket
import cv2
import pickle
from configuration import Configuration
import time
import io
from Job import Job
import random
import os
from pathlib import Path


class Client:
    """ TCP Client class """
    
    def __init__(self) -> None:
        self.configuration = Configuration()
        self.ip_address_server = self.configuration.get_config_param("network","ip_server")
        self.port_server = int(self.configuration.get_config_param("network","port_server"))
        self.buffer_size = int(self.configuration.get_config_param("comms","buffer_size"))
        self.id = random.randint(1,1000)
        #Calculating the ip
        self.get_ip()

        #Variables to load data and save it
        self.directoryToDo = str(Path().absolute())+self.configuration.get_config_param("server","directoryToDo")
        self.directoryToSave = str(Path().absolute())+self.configuration.get_config_param("server","directoryToSave")
        self.indexImage = 0
        #Elements to process on each job
        self.elements_load = int(self.configuration.get_config_param("server","elementsLoad"))
        

        #Creating the connection with the server
        self.server_address = (self.ip_address_server,self.port_server) 
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(self.server_address)
        
        #Waiting for the thread to finish
       
        print("Client finished")

    def send_job(self) -> None:
       """Function to create a new job"""
       if self.check_missing_payload:
        #Loading data
        payload = self.load_payload()
        if len(payload)>0:
            #Building the job object
            job = Job(payload,self.client_id,self.ip)
            #Sending data
            self.send_data(job)
        else:
            print("There is no missing payload to process")

    def get_ip (self):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]
        s.close()

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
        print(self.directoryToDo)
        listed_directory = os.listdir(self.directoryToDo)
        payload_process = []
        i  = 0
        for element in listed_directory:
            if i< self.elements_load:
                image= cv2.imread(self.directoryToDo+"\\"+element)
                i=i+1
                payload_process.append(image)
                #The image is deleted
                #os.remove(self.directoryToDo+"\\"+element)
                
            else:
                break
        print("Payload loaded")
        return payload_process

    def save_payload(self,payload):
        """Function to save the results of the processing"""
        for element in payload:
            #Writing the image
            print(self.directoryToSave+"\\"+str(self.indexImage)+".jpg")
            cv2.imwrite(self.directoryToSave+"\\"+str(self.indexImage)+".jpg",element)
            #Incrementing the index by one
            self.indexImage = self.indexImage+1

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

    def send_data(self,data):
    
        payload = pickle.dumps(data)
        n_bytes = self.socket_client.send(str(len(payload)).encode() + b"\r")
        self.socket_client.sendall(payload) 
        
      

if __name__ == "__main__":
    client = Client()
    try:
        while True:
            client.sendJob()
    except KeyboardInterrupt:
        print("Client finished")
    