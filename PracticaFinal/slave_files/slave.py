import socket
import pickle
from task_modules.image_task_module import ImageTaskModule
from configuration import Configuration
from job import Job
import io
import time
import os
from typing import Any
import cv2

# TODO: CHECK THE PATH BEFORE EXPORTING TO DOCKER
# -----------------------------------------------
import pathlib

FILE_PATH = f"{pathlib.Path(__file__).parent.resolve()}"
# -----------------------------------------------

MAX_CONNECTION_TRIES = 5

class Slave():
    """ 
        Slave Node class: Instances of this class perform the task/jobs requested by clients. Functionality:
        * Slave node must have `at least one task module`. Task modules contain are the only objets that know how to handle task.  
        * An incoming task is sent to the correspondant task module. All the task of the same type are handled by the same Slave node's task module of that type task. 
        * One node `can only be connected to a master`
        * The configuration for this class is at slave_config.ini file
    """
    
    def __init__(self) -> None:
        # Creates a configuration class to read/write config file
        self._configuration = Configuration(os.path.join(FILE_PATH,"slave_config.ini")) # TODO: Al levantarlo en un docker se deberia cambiar el path
        self._master_ip = self._configuration.get_config_param("Master","ip") # Node ip address
        self._master_port = int(self._configuration.get_config_param("Master","port")) # Node port 
        self._slave_buffer_size = int(self._configuration.get_config_param("Slave","buffer_size")) # Buffer size
        # Creates the socket of the slave
        self._slave_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def connect_to_master(self, max_connection_tries = 5) -> bool:
        """ 
            Attemps to stablish a connection with the master node. 
            If the number of tries exceeds the maximum indicated `max_connection_tries`, the connection is aborted.
            After a failed try, it waits 100ms until next. 
        """
        n_try = 0
        success = False
        while n_try < max_connection_tries and not success:
            try:
                # Attemps to connect to the master node
                self._slave_socket.connect((self._master_ip,self._master_port))
                success = True
            except ConnectionRefusedError:
                # Waits un 
                time.sleep(0.1)
                n_try += 1
        if success:
            print(f"Slave has successfully connected to Master node at {self._master_ip}:{self._master_port}.")
        else:
            print(f"Slave could not connect to Master node. Please check if the master node is active and it's direction is the one indicated {self._master_ip}:{self._master_port}.")
        return success
       
    def start(self) -> None:
        """ Stablish a socket connection with the master node and starts to communicate. """
        # Tries to connect to the master node
        connected =self.connect_to_master(MAX_CONNECTION_TRIES)
        # Socket infinite loop.
        while connected:
            # # Sends the server information about the slave capacities
            # payload = pickle.dumps("Hello Server!")
            # self._slave_socket.send(payload)
            # Receives a new job from server
            job_to_process = self.recieve_data()
            print("Job recieved")
            if job_to_process.job_type == "process.image.color_to_gray":
                task = ImageTaskModule()
                # Loads the data to the task module
                images = job_to_process.payload
                print(len(images))
                task.load_images(images)
                # Process the data
                payload_processed = task.do_task()
                # Loads the payload on the object to return
                job_to_process.payload = payload_processed
                job_to_process.done = True
                # Returns the object
                self.send_data(job_to_process)
                # waits for the confirmation of the msg
                msg = self.recieve_data()
                if msg == "Ok":
                    self.send_data("Ok")
                    print("Everything correct")
                    pass
                else:
                    break
                
    def send_data(self,data):
        payload = pickle.dumps(data)
        n_bytes = self._slave_socket.send(str(len(payload)).encode() + b"\r")
        self._slave_socket.sendall(payload) 

    def recieve_data(self) -> Job:
        try:
            n_bytes = b""
            byte = None
            while byte != b"\r":
                byte = self._slave_socket.recv(1)
                n_bytes += byte
            n_bytes = int(n_bytes)
            buffer = io.BytesIO()
            recibidos = 0
            print(n_bytes)
            while recibidos < n_bytes:
                msg = self._slave_socket.recv(self._slave_buffer_size)
                buffer.write(msg)
                recibidos += len(msg)
            buffer.seek(0)
            job = pickle.loads(buffer.read())
        except:
            print("Error")
        time.sleep(0.1)
        return job

if __name__ == "__main__":
    try:
        slave = Slave()
        slave.start()
    except KeyboardInterrupt:
        print("Client finished")
    
