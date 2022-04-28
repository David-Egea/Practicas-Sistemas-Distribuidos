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
from Job import Job

class ServerNode:
    
    def __init__(self):
        
        self.configuration = Configuration()
        self.ip_address = self.configuration.get_config_param('server',"ip")
        self.port = int(self.configuration.get_config_param("network","port_external"))
        self.buffer_size = int(self.configuration.get_config_param("comms","buffer_size"))

        
        self.indexImage = 0
                
        # The socket of the server is created
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Server binding
            self.server_socket.bind((self.ip_address,self.port))
        except:
            print(f"UPS! something went wrong. ({sys.exc_info()})")
            sys.exit()
    def activate(self):
         
        # The server starts to listen 
        print("The server node is listening on the port {}".format(self.port))
        self.server_socket.listen() 
        # infinite loop- do not reset for every requests
        while True:
            # Waiting a client
            client, (ip, port) = self.server_socket.accept()
            print(f"There is a client with the ip: {ip} and port {port}.")
            try:
                Thread(target=self.clientThread,args=(client,1024)).start()
            except:
                print("Thread creation has failed")
                traceback.print_exc()
    
    def checkMissingJob(self):
        """Function to check is there are any missing jobs to be done"""
        #TODO
    def save_job(self,flag,job):
        """Function to save a job"""
        if flag == 'Done':
            #First jobs are loaded
            jobs = self.load_jobs(flag)

            #The job is appended
            jobs.append(job)

            #Jobs are saved
            with open('done/jobs.list', 'wb') as fileSave:
                pickle.dump(jobs, fileSave)

        elif flag == 'ToDo':
            #First jobs are loaded
            jobs = self.load_jobs(flag)
            
            #The job is appended
            jobs.append(job)

            #Jobs are saved
            with open('done/jobs.list', 'wb') as fileSave:
                pickle.dump(jobs, fileSave)

    def load_jobs(self,flag):
        # TODO: revisar que el archivo exista, si no existe devolver una lista vacía
        """Function to load all the payload to process"""
        with open('done/jobs.list', 'rb') as fileLoad:
                jobs = pickle.load(fileLoad)
                fileLoad.close()
        print("Job loaded")
        return jobs

    def clientThread(self,client,dummy):
        #TODO: cambiar toda la lógica de guardado para adaptarla a jobs
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
