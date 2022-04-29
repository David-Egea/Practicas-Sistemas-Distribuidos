import socket
from threading import Thread, Lock
import sys
import traceback
import os
import cv2
from pathlib import Path
import pickle
from configuration import Configuration
import time 
import io
class ServerNode:
    
    def __init__(self):
        
        self.configuration = Configuration()
        self.ip_address = self.configuration.get_config_param('network',"ip")
        self.port = int(self.configuration.get_config_param("network","port"))
        self.buffer_size = int(self.configuration.get_config_param("comms","buffer_size"))

        self.directoryToDo = str(Path().absolute())+self.configuration.get_config_param("server","directoryToDo")
        self.directoryToSave = str(Path().absolute())+self.configuration.get_config_param("server","directoryToSave")
        self.indexImage = 0
        
        #Elements to process on each job
        self.elements_load = int(self.configuration.get_config_param("server","elementsLoad"))
        
        # The socket of the server is created
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Server binding
            server_socket.bind((self.ip_address,self.port))
        except:
            print(f"UPS! something went wrong. ({sys.exc_info()})")
            sys.exit()
        # The server starts to listen 
        print("The server node is listening on the port {}".format(self.port))
        server_socket.listen() 
        # infinite loop- do not reset for every requests
        while True:
            # Waiting a client
            client, (ip, port) = server_socket.accept()
            print(f"There is a client with the ip: {ip} and port {port}.")
            try:
                Thread(target=self.clientThread,args=(client,1024)).start()
            except:
                print("Thread creation has failed")
                traceback.print_exc()
    
    def checkMissingJob(self):
        """Function to check is there are any missing jobs to be done"""
       #TODO
    def save_payload(self,payload):
        """Function to save the results of the processing"""
      #TODO
    def loadJob(self):
        """Function to load all the payload to process"""
        print("Loading jobs")
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
        print("Job loaded")
        return payload_process
    def clientThread(self,client,dummy):
        """Function to manage the conection of each client"""
        global print_lock
        while True:
            #Check missing jobs
            if self.checkMissingJob():
                print("There are missing jobs")
                print_lock.acquire()
                payload = self.loadJob()
                print_lock.release()
                self.sendData(client,payload)
                print("Sended")

                #Wait to recieve a message from the node
                data = self.recieve_data(client)
                
                #Data is saved
                print_lock.acquire()
                self.save_payload(data)
                print_lock.release()
                print("Data saved")
                #Getting confirmation msg
                msg = self.recieve_data(client)
               
                print("Confirmation recieved {}".format(msg))
                if msg == "Ok":
                    print("Everything correct")
                    #Sending confirmation msg
                    conf_msg= "Ok"
                    self.sendData(client,conf_msg)
                else:
                    print("There is an error with the node")
    
                    break
    
    def recieve_data(self,client):
        try:
            n_bytes = b""
            byte = None
            while byte != b"\r":
                byte = client.recv(1)
                n_bytes += byte

            n_bytes = int(n_bytes)
            buffer = io.BytesIO()
            recibidos = 0
            while recibidos < n_bytes:
                msg = client.recv(self.buffer_size)
                buffer.write(msg)
                recibidos += len(msg)
            buffer.seek(0)
            data = pickle.loads(buffer.read())
            print(data)
        except:
            print("Error")
        time.sleep(0.1)
        return data
    def sendData(self,client,data):
    
        payload = pickle.dumps(data)
        n_bytes = client.send(str(len(payload)).encode() + b"\r")
        client.sendall(payload) 
        
if __name__ == "__main__":
    global print_lock
    print_lock = Lock()
    #An object of node type is created
    nodo = ServerNode()
