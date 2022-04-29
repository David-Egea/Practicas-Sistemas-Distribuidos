import socket
from threading import Thread, ThreadError
import sys
import traceback
from pathlib import Path
from multiprocessing import Process,Manager
from configuration.configuration import Configuration
from service_server import ServiceServer
from master_node import MasterNode

# TODO: CAMBIAR ESTA CLASE PARA QUE SEA EL SERVIDOR

class Server:
    """ 
        Master Node class. Each Distributed Computing Network must have `one and only one instance` of this class. Functionality:
        * Does not performs the commanded task itself, instead it sends it to the Slave Nodes connected.
        * Stablishes and disconnects the connections.
        * The only element in the network which communicates with the client
    """
    
    def __init__(self):
        # Creates a configuration class
        self._config = Configuration(config_file_path=str(f"{Path()}\\PracticaFinal\\configuration\\config.ini"))
       
        self.master_node = MasterNode()
        self.server_node = ServiceServer()

    def start(self) -> None:
        """ Starts running the master node on the address specified. """
        # Creates a new process for server interface activation 
        self._master_process = Process(target=self.master_node.activate(), args=())
        self._master_process.start()
        # Creates a new process for server interface activation 
        self._server_process = Process(target=self.server_node.activate(), args=())
        self._server_process.start()
    

    def stop(self) -> None:
        """ Interrupts the master node."""
        self._master_process.join()
        self._server_process.join()
        self._master_process.close()
        self._server_process.close()


