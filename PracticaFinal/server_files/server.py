import socket
from threading import Thread, ThreadError
import sys
import traceback
from pathlib import Path
from multiprocessing import Process
from configuration.configuration import Configuration

# TODO: CAMBIAR ESTA CLASE PARA QUE SEA EL SERVIDOR

class Server:
    """ 
        Master Node class. Each Distributed Computing Network must have `one and only one instance` of this class. Functionality:
        * Does not performs the commanded task itself, instead it sends it to the Slave Nodes connected.
        * Stablishes and disconnects the connections.
        * The only element in the network which communicates with the client
    """
    
    def __init__(self):
        # Creates a list for registered clients
        self._client_list = []
        # Creates a list for registered slave nodes
        self._slave_nodes_list = []
        # Creates a configuration class
        self._config = Configuration(config_file_path=str(f"{Path()}\\PracticaFinal\\configuration\\config.ini"))
        # Master node configuration
        self._master_ip = str(self._config.get_config_param("Master","ip"))
        self._master_port = int(self._config.get_config_param("Master","port"))
        self._master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._master_buffer_size = 4096 # Master's socket buffer size
        try:
            # Attempts to bind the direction to the address
            self._master_socket.bind((self._master_ip,self._master_port)) # Server binding
        except:
            print(f"[Error] An exception ocurred during master socket binding. ({sys.exc_info()})")
            sys.exit()
        # Server node configuration
        self._server_ip = str(self._config.get_config_param("Server","ip")) # Master node IP address
        self._server_port = int(self._config.get_config_param("Server","port")) # Master node port address
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_buffer_size = 4096 # Server's socket buffer size
        try:
            # Attempts to bind the direction to the address
            self._server_socket.bind((self._server_ip,self._server_port)) # Server binding
        except:
            print(f"[Error] An exception ocurred during server socket binding. ({sys.exc_info()})")
            sys.exit()

    def start(self) -> None:
        """ Starts running the master node on the address specified. """
        # Creates a new process for server interface activation 
        self._master_process = Process(target=self.activate_master_interface, args=())
        self._master_process.start()
        # Creates a new process for server interface activation 
        self._server_process = Process(target=self.activate_server_interface, args=())
        self._server_process.start()

    def stop(self) -> None:
        """ Interrupts the master node."""
        self._master_process.join()
        self._server_process.join()
        self._master_process.close()
        self._server_process.close()

    def activate_master_interface(self) -> None:
        """ Starts listening to available slave nodes, stablishing a communication with each of them. """
        self._master_socket.listen() # Master starts to listen on port
        print(f"The server node at {self._master_ip} is listening on port {self._master_port}...")
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

    def activate_server_interface(self) -> None:
        """ Starts listening to available clients, stablishing a communication with each of them. """
        self._server_socket.listen() # Server starts to listen on port
        print(f"The server node at {self._server_ip} is listening on port {self._server_port}...")
        # infinite loop-do not reset for every requests
        while True:
            # Waits until a new client connection
            client_socket, (client_ip, client_port) = self._master_socket.accept()
            print(f"There is a client with the ip: {client_ip} and port {client_port}.")
            try:
                # Creates a thread for that client connection
                Thread(target=self.client_connection, args=(client_socket,1024)).start()
            except ThreadError:
                print("[Error] Thread creation failed!")
                traceback.print_exc()