import socket
import pickle
from job import Job
from configuration import Configuration
from pathlib import Path
import io
import time

class SlaveNode:
    """ 
        Slave Node class: Instances of this class perform the task/jobs requested by clients. Functionality:
        * Slave node must have `at least one task module`. Task modules contain are the only objets that know how to handle task.  
        * An incoming task is sent to the correspondant task module. All the task of the same type are handled by the same Slave node's task module of that type task. 
        * One node `can only be connected to a master`
        * The configuration for this class is at slave_config.ini file
    """
    
    def __init__(self) -> None:
        # Creates a configuration class to read/write config file
        self._configuration = Configuration("C:\\Users\\Raul\\Documents\\Github\\Practicas-Sistemas-Distribuidos\\PracticaFinal\\slave_files\\slave_config.ini") # TODO: Al levantarlo en un docker se deberia cambiar el path
        self._master_ip = self._configuration.get_config_param("Master","ip") # Node ip address
        self._master_port = int(self._configuration.get_config_param("Master","port")) # Node port 
        self._slave_buffer_size = int(self._configuration.get_config_param("Slave","buffer_size")) # Buffer size
        # Creates the socket of the slave
        self._slave_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.master_address = (self._master_ip,self._master_port) 

        # Connects to the master node
        self._slave_socket.connect(self.master_address)
        # If the connection is succecfull, the thread starts
        self.start()

    def start(self) -> None:
        """ Stablish a socket connection with the master node and starts to communicate. """
       
        # Socket infinite loop.
        while True:
            # # Sends the server information about the slave capacities
            # payload = pickle.dumps("Hello Server!")
            # self._slave_socket.send(payload)
            
            # Receives a new job from server
            new_job = self.recieve_data()
            print("Job recieved")

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
        slave = SlaveNode()
 
    except KeyboardInterrupt:
        print("Client finished")
    
