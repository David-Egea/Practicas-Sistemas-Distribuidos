import socket
from threading import Thread, Lock
import sys
import traceback
import os
from pathlib import Path
import pickle
import numpy as np

from numpy import true_divide
from configuration import Configuration
import time 
import io
from utils.job import Job

class ServiceServer:
    """ 
        Service Server class: Instances of this class perform server functionality. Functionality:
        * The server recieves requests from clients      * The configuration for this class is at slave_config.ini file

            """
    def __init__(self):
        
        self.configuration = Configuration()
        self.ip_address = self.configuration.get_config_param('server',"ip")
        self.port = int(self.configuration.get_config_param("network","port_external"))
        self.buffer_size = int(self.configuration.get_config_param("comms","buffer_size"))

        
        self.elements_load = int(self.configuration.get_config_param("comms","buffer_size")) 

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
        """ Function to activate the server service node"""
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
        """Function to save a job"""
        if flag == 'Done':
            #First jobs are loaded
            jobs = self.load_jobs(flag)

            #The job is appended
            jobs.append(job)

            #Jobs are saved
            with open('ResponseOutBox/jobs.list', 'wb') as fileSave:
                pickle.dump(jobs, fileSave)

        elif flag == 'ToDo':
            #First jobs are loaded
            jobs = self.load_jobs(flag)
            
            #The job is appended
            jobs.append(job)

            #Jobs are saved
            with open('TaskInbox/jobs.list', 'wb') as fileSave:
                pickle.dump(jobs, fileSave)

    def is_job_done(self,client_id):
        # TODO: adaptarlo a jobs fragmentados
        # First all the jobs are loaded
        jobs_return = []
        jobs_loaded = self.load_jobs("Done")
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
                    
                    return True,job_joined
            else:
                return True,jobs_return[0]
        else:    
            return False

    def load_jobs(self,flag):
        # TODO: revisar que el archivo exista, si no existe devolver una lista vacía
        """Function to load all the payload to process"""
        if flag == "Done":
            with open('ResponseOutBox/jobs.list', 'rb') as fileLoad:
                if len(os.listdir("/done"))>0:
                    jobs = pickle.load(fileLoad)
                    fileLoad.close()
                else:
                    jobs = []
        elif flag == "ToDo":   
            with open('TaskInbox/jobs.list', 'rb') as fileLoad:
                if len(os.listdir("/done"))>0:
                    jobs = pickle.load(fileLoad)
                    fileLoad.close()
                else:
                    jobs = []
        print("Job loaded")
        return jobs
    
    def fragment_job(self,job):
        """Function to check if a job needs to be fragmented"""
        jobs_fragmented = []
        if len(job.payload)>self.elements_load:
            
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
                jobs_fragmented.append(new_job)
        else:
            jobs_fragmented.append(job)

        return jobs_fragmented



    def clientThread(self,client,dummy):
        """Function to manage the conection of each client"""
        global print_lock
        while True:
            # Waits to recieve a job from the client
            job_to_do = self.recieve_data(client)
            jobs_fragmented = self.fragment_job(job_to_do)
            # Getting the client id
            client_id = job_to_do.client_id
            #The job is in the list to be done
            for job_to_save in jobs_fragmented:    
                self.save_job("ToDo",job_to_save)
            print("Jobs saved")

            # Waits to get the job done
            while not self.is_job_done(client_id)[0]:
                pass
            print("Job finished")
            # The job is sended to the client
            job_to_send = self.is_job_done(client_id)[1]
            self.send_data(client,job_to_send)
            # Waits for the confirmation msg
            msg = self.recieve_data(client)

            if msg == "Ok":
                print("Everything correct")
                # Sending confirmation msg
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
    def send_data(self,client,data):
    
        payload = pickle.dumps(data)
        n_bytes = client.send(str(len(payload)).encode() + b"\r")
        client.sendall(payload) 
        
if __name__ == "__main__":
    global print_lock
    print_lock = Lock()
    # An object of node type is created
    nodo = ServiceServer()
