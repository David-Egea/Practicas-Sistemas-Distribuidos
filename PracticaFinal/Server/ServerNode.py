import socket
from threading import Thread, Lock
import sys
import traceback
import os
import cv2
from pathlib import Path
import pickle

class ServerNode:
    
    def __init__(self):
        
        self.ip = "localhost"
        self.port = 6000
        self.directoryToDo = str(Path().absolute())+"\\PracticaFinal\\Server\\filesToDo"
        self.directoryToSave = str(Path().absolute())+"\\PracticaFinal\\Server\\filesDone"
        self.indexImage = 0
        self.buffer_size = 4096
        #Elements to process on each job
        self.elements_load = 1
        
        # The socket of the server is created
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Server binding
            server_socket.bind((self.ip,self.port))
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
        listed_directory = os.listdir(self.directoryToDo)
        if len(listed_directory)>0:
            return True
        else:
            return False
    def save_payload(self,payload):
        """Function to save the results of the processing"""
        for element in payload:
            #Writing the image
            print(self.directoryToSave+"\\"+str(self.indexImage)+".jpg")
            cv2.imwrite(self.directoryToSave+"\\"+str(self.indexImage)+".jpg",element)
            #Incrementing the index by one
            self.indexImage = self.indexImage+1
    def loadJob(self):
        """Function to load all the payload to process"""
        print("Loading jobs")
        print(self.directoryToDo)
        listed_directory = os.listdir(self.directoryToDo)
        payload_process = []
        i  = 0
        for element in listed_directory:
            if i<= self.elements_load:
                image= cv2.imread(self.directoryToDo+"\\"+element)
                payload_process.append(image)
                #The image is deleted
                #os.remove(self.directoryToDo+"\\"+element)
                i=+1
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
                payload = pickle.dumps(payload)
                client.sendall(payload)
                print("Sended")

                #Wait to recieve a message from the node
                data = self.recieve_data(client)
                data = pickle.loads(data)
                #Data is saved
                print_lock.acquire()
                self.save_payload(data)
                print_lock.release()

                #Getting confirmation msg
                msg = self.recieve_data(client)
                msg = pickle.loads(msg)

                if msg == "Ok":
                    print("Everything correct")
                    #Sending confirmation msg
                    conf_msg= "Ok"
                    conf_msg = pickle.dumps(conf_msg)
                    client.sendall(conf_msg)
                else:
                    print("There is an error with the node")
    
                    break
    def recieve_data(self,client):
        data = bytearray()
        client.setblocking(True)
        try:
            while True:
                data +=bytearray((client.recv(self.buffer_size)))
                # A partir de ahora si no hay datos que leer finalizamos el bucle
                client.setblocking(False)
        except socket.error:
            print("Datos terminados")
            client.setblocking(True)
            return data
if __name__ == "__main__":
    global print_lock
    print_lock = Lock()
    #An object of node type is created
    nodo = ServerNode()
