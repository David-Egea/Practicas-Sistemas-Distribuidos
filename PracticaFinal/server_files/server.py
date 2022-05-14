from multiprocessing import Process
from configuration.configuration import Configuration
from server_files.service_server import ServiceServer
from server_files.master_node import MasterNode
import os

# TODO: CHECK THE PATH BEFORE EXPORTING TO DOCKER
# -----------------------------------------------
import pathlib

FILE_PATH = f"{pathlib.Path(__file__).parent.resolve()}"
# -----------------------------------------------

class Server:
    """ 
        Master Node class. Each Distributed Computing Network must have `one and only one instance` of this class. Functionality:
        * Does not performs the commanded task itself, instead it sends it to the Slave Nodes connected.
        * Stablishes and disconnects the connections.
        * The only element in the network which communicates with the client
    """
    
    def __init__(self):
        # Creates a configuration class
        self._config = Configuration(os.path.join(FILE_PATH,"server_config.ini"))
        # Creates an instance of Master Node for task management
        self.master_node = MasterNode()
        # Craetes an instance of Service Server for request
        self.server_node = ServiceServer()

    def start(self) -> None:
        """ Starts running the master node on the address specified. """
        # Creates a new process for server interface activation 
        self._master_process = Process(target=self.master_node.activate, args=())
        # Creates a new process for server interface activation 
        self._server_process = Process(target=self.server_node.activate, args=())
        self._master_process.start()
        self._server_process.start()
        # Waits until processes are finished
        self._master_process.join()
        self._server_process.join()

    def stop(self) -> None:
        """ Interrupts the master node. """
        self._master_process.close()
        self._server_process.close()

if __name__ == "__main__":
    try:
        server = Server()
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print("Client finished")

