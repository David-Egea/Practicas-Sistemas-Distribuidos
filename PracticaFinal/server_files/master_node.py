import socket
from threading import Thread, ThreadError
import sys
import traceback
from pathlib import Path
from multiprocessing import Process

from zmq import EVENT_CLOSE_FAILED
from configuration import Configuration
import pickle
import os
import time
import io

# TODO:Checkear que las funciones son correctas
class MasterNode:
    """ 
        Master Node class. Each Distributed Computing Network must have `one and only one instance` of this class. Functionality:
        * Does not performs the commanded task itself, instead it sends it to the Slave Nodes connected.
        * Stablishes and disconnects the connections.
        * The only element in the network which communicates with the client
    """
    
    def __init__(self):
        # Creates a list for registered slave nodes
        self._slave_nodes_regist = {}
        # Creates a configuration class
        self._config = Configuration("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\server_config.ini")
        # Master node configuration
        self._master_ip = str(self._config.get_config_param("master","ip"))
        self._master_port = int(self._config.get_config_param("master","port_external"))
        # Creating the socket
        self._master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = int(self._config.get_config_param("comms","buffer_size"))

        try:
            # Attempts to bind the direction to the address
            self._master_socket.bind((self._master_ip,self._master_port)) # Server binding
        except:
            print(f"[Error] An exception ocurred during master socket binding. ({sys.exc_info()})")
            sys.exit()


    def stop(self) -> None:
        """ Interrupts the master node."""
        self._master_process.join()
        self._master_process.close()

    def check_missing_jobs(self):
        """Function to check is there are any missing jobs to be done"""
        print(os.listdir("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\TaskInbox"))
        if len(os.listdir("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\TaskInbox"))>0:
            jobs  = self.load_jobs("ToDo")
            if len(jobs)>0:
                print("There are missing jobs")
                return True
            else:
                return False
        else:
            return False
      

    def activate(self) -> None:
        """ Starts listening to available slave nodes, stablishing a communication with each of them. """
        self._master_socket.listen() # Master starts to listen on port
        print(f"The master node at {self._master_ip} is listening on port {self._master_port}...")
        # infinite loop-do not reset for every requests
        while True:
            # Waits until a new client connection
            slave_socket, (slave_ip, slave_port) = self._master_socket.accept()
            print(f"There is a slave with the ip: {slave_ip} and port {slave_port}.")
            try:
                # Creates a thread for that client connection
                Thread(target=self.slave_connection, args=(slave_socket,1024)).start()
            except ThreadError:
                print("[Error] Thread creation failed!")
                traceback.print_exc()

    def save_job(self,flag,job):
        """Function to save a job"""
        if flag == 'Done':
            #First jobs are loaded
            jobs = self.load_jobs(flag)

            #The job is appended
            jobs.append(job)

            #Jobs are saved
            with open("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\ResponseOutBox\\jobs.list", 'wb') as fileSave:
                pickle.dump(jobs, fileSave)

        elif flag == 'ToDo':
            #First jobs are loaded
            jobs = self.load_jobs(flag)
            
            #The job is appended
            jobs.append(job)

            #Jobs are saved
            with open("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\TaskInbox\\jobs.list", 'wb') as fileSave:
                pickle.dump(jobs, fileSave)

    def load_jobs(self,flag):
        # TODO: revisar que el archivo exista, si no existe devolver una lista vacía
        """Function to load all the payload to process"""
        if flag == "Done":
            if len(os.listdir("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\ResponseOutBox"))>1:
                with open("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\ResponseOutBox\\jobs.list", 'rb') as fileLoad:
                        jobs = pickle.load(fileLoad)
                        fileLoad.close()
            else:
                jobs = []
        elif flag == "ToDo":  
            if len(os.listdir("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\TaskInbox"))>0: 
                with open("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\TaskInbox\\jobs.list", 'rb') as fileLoad:               
                    jobs = pickle.load(fileLoad)
                    fileLoad.close()
            else:
                jobs = []
        print("Job loaded")
        return jobs

    def delete_job(self,job_delete):
        """Function to delete an specific job"""
        jobs_save = []
        #First loads all the jobs
        jobs = self.load_jobs("ToDo")
        for job in jobs:
            if job.id == job_delete.id:
                print("Job Equal")
                pass
            else:
                jobs_save.append(job)
        # Saves the jobs
        with open("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\server_files\\TaskInbox\\jobs.list", 'wb') as fileSave:
            pickle.dump(jobs_save, fileSave)
        
    def load_job_to_process(self):
        """ Function that loads a job, and deletes it from the list"""
        jobs = self.load_jobs("ToDo")
        # Gets the job to process
        job_to_process = jobs[0]
        # Deteletes the job
        self.delete_job(jobs[0])

        return job_to_process

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


    def slave_connection(self, slave_socket: socket.socket,dummy): 
   
        while True:
            # Checks if there are jobs to do
            if self.check_missing_jobs():
                # Loads the job
                
                job_to_do = self.load_job_to_process()
                
                # Sends the job
                self.send_data(slave_socket,job_to_do)
                #   Waits for the job to be done
                job_done = self.recieve_data(slave_socket)
                # Saves the job
                self.save_job("Done",job_done)
                # Sends the ok command
                self.send_data(slave_socket,"Ok")
                # Waits for the confirmation from the slave
                conf_msg = self.recieve_data(slave_socket)
                if conf_msg == "Ok":
                    pass
                else:
                    print("There is an error with the slave")
                    # TODO: Guardar el trabajo no realizado
                    break
