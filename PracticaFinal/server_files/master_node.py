import socket
from threading import Thread, ThreadError
import sys
import traceback
from typing import Any, List
from job import Job
from configuration import Configuration
import pickle
import os
import time
import io

# TODO: CHECK THE PATH BEFORE EXPORTING TO DOCKER
# -----------------------------------------------
import pathlib

FILE_PATH = f"{pathlib.Path(__file__).parent.resolve()}"
# -----------------------------------------------

class MasterNode:
    """ 
        Master Node class. Each Distributed Computing Network must have `one and only one instance` of this class. Functionality:
        * Does not performs the commanded task itself, instead it sends it to the Slave Nodes connected.
        * Stablishes and disconnects the connections.
        * The only element in the network which communicates with the client
    """
    
    def __init__(self):
        # Configurates basic parameters of Service Server
        self._slave_nodes_regist = {}
        # Creates a configuration class
        self._config = Configuration(os.path.join(FILE_PATH,"server_config.ini"))
        # Master node configuration
        self._master_ip = str(self._config.get_config_param("master","ip"))
        self._master_port = int(self._config.get_config_param("master","port_external"))
        # Creating the socket
        self._master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = int(self._config.get_config_param("comms","buffer_size"))
        self.index_job = 0

        try:
            # Attempts to bind the direction to the address
            self._master_socket.bind((self._master_ip,self._master_port)) # Server binding
        except:
            print(f"[Error] An exception ocurred during master socket binding. ({sys.exc_info()})")
            sys.exit()

    def check_missing_jobs(self) -> bool:
        """ Function to check is there are any missing jobs to be done. 
            Returns True if there is any job to do, returns False otherwise. 
        """
        if len(os.listdir(os.path.join(FILE_PATH,"TaskInbox")))>0:
            print("There are missing jobs")
            return True
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
        """Function to save a job. """
        if flag == 'Done':
            name = "job"+str(self.index_job)+".list"
            with open(os.path.join(FILE_PATH,"ResponseOutBox",name), 'wb') as fileSave:
                pickle.dump(job, fileSave)
                fileSave.close()
            self.index_job = self.index_job+1
            print("Job Done saved")
        elif flag == 'ToDo':
            name = "job"+str(self.index_job)+".list"
            with open(os.path.join(FILE_PATH,"TaskInbox",name), 'wb') as fileSave:
                pickle.dump(job, fileSave)
                fileSave.close()
            self.index_job = self.index_job+1

    
    def delete_job(self,job_delete):
        """Function to delete an specific job"""
        for element in os.listdir(os.path.join(FILE_PATH,"TaskInbox")):
            with open(os.path.join(FILE_PATH,"TaskInbox",element), 'rb') as fileLoad:
                job = pickle.load(fileLoad)
                fileLoad.close()
            if job.id == job_delete.id:
                os.remove(os.path.join(FILE_PATH,"TaskInbox",element))

        
    def load_job(self,flag):
        # TODO: revisar que el archivo exista, si no existe devolver una lista vacía
        """Function to load all the payload to process"""
        job = None
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
                job = None
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
                job = None
        return job

    def recieve_data(self,client: socket.socket) -> Any:
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

    def send_data(self, client: socket.socket, data: Any) -> None:
        payload = pickle.dumps(data)
        client.send(str(len(payload)).encode() + b"\r")
        client.sendall(payload) 

    def slave_connection(self, slave_socket: socket.socket,dummy): 
        while True:
            # Checks if there are jobs to do
            if self.check_missing_jobs():
                # Loads the job
                job_to_do = self.load_job("ToDo")
                if job_to_do!=None:
                    # Sends the job
                    self.send_data(slave_socket,job_to_do)
                    # Waits for the job to be done
                    job_done = self.recieve_data(slave_socket)
                    # Saves the job
                    self.save_job("Done",job_done)
                    # Sends the ok command
                    self.send_data(slave_socket,"Ok")
                    self.delete_job(job_done)
                    # Waits for the confirmation from the slave
                    conf_msg = self.recieve_data(slave_socket)
                    if conf_msg == "Ok":
                        print("Everything went ok")
                        pass
                    else:
                        print("There is an error with the slave")
                        # TODO: Guardar el trabajo no realizado
                        break
