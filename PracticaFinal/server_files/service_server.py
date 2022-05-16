import socket
from threading import Thread, Lock
from typing import Any
import sys
import traceback
import os
import pickle
import numpy as np
import random
from configuration import Configuration
import time 
import io
from job import Job

# TODO: CHECK THE PATH BEFORE EXPORTING TO DOCKER
# -----------------------------------------------
import pathlib

FILE_PATH = f"{pathlib.Path(__file__).parent.resolve()}"
# -----------------------------------------------

class ServiceServer:
    """ 
        Service Server class: Instances of this class perform server functionality. Functionality:
        * The server recieves requests from clients     
        * The configuration for this class is at slave_config.ini file
    """

    def __init__(self):
        # Configurates basic parameters of Service Server
        self.configuration = Configuration(os.path.join(FILE_PATH,"server_config.ini"))
        self.ip_address = self.configuration.get_config_param('server',"ip")
        self.port = int(self.configuration.get_config_param("server","port_external"))
        self.buffer_size = int(self.configuration.get_config_param("comms","buffer_size"))
        self.elements_load = int(self.configuration.get_config_param("comms","buffer_size")) 
        # Index to save the jobs
        self.index_job = 0
        # The socket of the server is created
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        try:
            # Binds socket address
            self.server_socket.bind((self.ip_address,self.port))
        except:
            print(f"UPS! something went wrong. ({sys.exc_info()})")
            sys.exit()

    def activate(self) -> None:
        """ Function to activate the server service node. """
        # The server starts to listen 
        print("The server node is listening on the port {}".format(self.port))
        self.server_socket.listen() 
        #Iinfinite loop- do not reset for every requests
        while True:
            # Waiting a client
            client, (ip, port) = self.server_socket.accept()
            print(f"There is a client with the ip: {ip} and port {port}.")
            try:
                Thread(target=self.clientThread,args=(client,1024)).start()
            except:
                print("Thread creation has failed")
                traceback.print_exc()
   
    def save_job(self,flag,job):
        """Function to save a job. """
        if flag == 'Done':
            name = "job"+str(self.index_job)+".list"
            with open(os.path.join(FILE_PATH,"ResponseOutBox",name), 'wb') as fileSave:
                pickle.dump(job, fileSave)
                fileSave.close()
            self.index_job = self.index_job+1
        elif flag == 'ToDo':
            name = "job"+str(self.index_job)+".list"
            with open(os.path.join(FILE_PATH,"TaskInbox",name), 'wb') as fileSave:
                pickle.dump(job, fileSave)
                fileSave.close()
            self.index_job = self.index_job+1

    def is_job_done(self,client_id):
        # TODO: adaptarlo a jobs fragmentados
        # First all the jobs are loaded
        """
        jobs_return = []
        jobs_loaded = self.load_job("Done")
        fragmented = False
        for job in jobs_loaded:
            if job.client_id == client_id:
                # Checks for all the jobs needed
                jobs_return.append(job)
                if job.fragments>1:
                    fragmented = True
                    fragments = job.fragments
        if len(jobs_return)>0:
            if fragmented:
                # If the job is fragmented, checks for all the pieces in the sequence
                if len(jobs_return) != fragments:
                    return False
                else:
                    #Creating 
                    payload_joined = []
                    for job_join in jobs_return:
                        payload_joined.append(job_join.payload())
                    job_joined = Job(jobs_return[0].client_id,jobs_return[0].job_type,payload_joined)
                    print("Job Found")
                    self.delete_job(jobs_return)

                    return True,job_joined
            else:
                print("Job found")
                return True,jobs_return[0]
        else:    
            return False
        """
        if len(os.listdir(os.path.join(FILE_PATH,"ResponseOutBox")))>0:
            for element in os.listdir(os.path.join(FILE_PATH,"ResponseOutBox")):
                with open(os.path.join(FILE_PATH,"ResponseOutBox",element), 'rb') as fileLoad:
                        job = pickle.load(fileLoad)
                        fileLoad.close()
                if job.client_id == client_id:
                    self.delete_job(job)
                    return job
        return None

    def delete_job(self,job_delete):
        """Function to delete an specific job"""
        for element in os.listdir(os.path.join(FILE_PATH,"ResponseOutBox")):
            with open(os.path.join(FILE_PATH,"ResponseOutBox",element), 'rb') as fileLoad:
                job = pickle.load(fileLoad)
                fileLoad.close()
            if job.id == job_delete.id:
                os.remove(os.path.join(FILE_PATH,"ResponseOutBox",element))

    def load_job(self,flag):
        # TODO: revisar que el archivo exista, si no existe devolver una lista vacía
        """Function to load all the payload to process"""
        job = []
        if flag == "Done":
            if len(os.listdir(os.path.join(FILE_PATH,"ResponseOutBox")))>0:
                elements = os.listdir(os.path.join(FILE_PATH,"ResponseOutBox"))
                try:
                    with open(os.path.join(FILE_PATH,"ResponseOutBox",elements[0]), 'rb') as fileLoad:
                        job = pickle.load(fileLoad)
                        fileLoad.close()
                except:
                    pass
            else:
                job = []
        elif flag == "ToDo":   
            if len(os.listdir(os.path.join(FILE_PATH,"TaskInbox")))>0:
                elements = os.listdir(os.path.join(FILE_PATH,"TaskInbox"))
                try:
                    with open(os.path.join(FILE_PATH,"TaskInbox",elements[0]), 'rb') as fileLoad:
                        job = pickle.load(fileLoad)
                        fileLoad.close()
                except:
                    pass
            else:
                job = []
        return job
    
    def fragment_job(self, job: Job):
        """Function to check if a job needs to be fragmented"""
        jobs_fragmented = []
        if len(job.payload) > self.elements_load:
            # Calculating the number of jobs to create
            fragments = np.ceil(len(job.payload)/self.elements_load)
            # Iterating over the number of fragments
            actual_fragment = 0
            for i in range(0,fragments):
                # Calculating the number of elements 
                if actual_fragment+self.elements_load>=len(job.payload):
                    calculated_payload = job.payload[actual_fragment:len(len(job.payload))]
                else:
                    calculated_payload = job.payload[actual_fragment:actual_fragment+self.elements_load]
                actual_fragment = actual_fragment+self.elements_load
                new_job = Job(job.client_id,job.job_type,calculated_payload)
                #adding the control variables
                new_job.sequence = i
                new_job.fragments = fragments
                id = random.randint(0,1000)
                new_job.id = id
                jobs_fragmented.append(new_job)
        else:
            id = random.randint(0,1000)
            job.id = id
            jobs_fragmented.append(job)
        print("Jobs fragmented = {}".format(len(jobs_fragmented)))
        return jobs_fragmented

    def clientThread(self, client: socket.socket,dummy):
        """Function to manage the conection of each client"""
        global print_lock
        while True:
            elements_sended = 0
            # Waits to recieve a job from the client
            job_to_do = self.recieve_data(client)
            jobs_fragmented = self.fragment_job(job_to_do)
            fragments = len(jobs_fragmented)
            print(len(jobs_fragmented))
            # Getting the client id
            client_id = job_to_do.client_id
            #The job is in the list to be done
            for job_to_save in jobs_fragmented:    
                self.save_job("ToDo",job_to_save)
            print("Jobs saved")

            while elements_sended<fragments:
                # Waits to get the job done
                job_done = self.is_job_done(client_id)
                while job_done==None:
                    job_done = self.is_job_done(client_id)
                    
                print("Job finished")
                # The job is sended to the client
                self.send_data(client,job_done)
                elements_sended = elements_sended+1
                # Waits for the confirmation msg
                msg = self.recieve_data(client)
                if msg == 'Ok':
                    pass
                else:
                    print("There is an error with the node")

                    break
           
            print("Everything correct")
            # Sending confirmation msg
            conf_msg= "Ok"
            self.send_data(client,conf_msg)
        
    
    def recieve_data(self, client: socket.socket):
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
        except:
            print("Error")
        time.sleep(0.1)
        return data

    def send_data(self, client: socket.socket, data: Any):
        payload = pickle.dumps(data)
        n_bytes = client.send(str(len(payload)).encode() + b"\r")
        client.sendall(payload) 
        
if __name__ == "__main__":
    global print_lock
    print_lock = Lock()
    # An object of node type is created
    nodo = ServiceServer()
    nodo.activate()
