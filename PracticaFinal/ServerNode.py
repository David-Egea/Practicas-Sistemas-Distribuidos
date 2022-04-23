import socket
from threading import Thread, Lock
import sys
import traceback

class ServerNode:
    def clientThread(self,client):
        
        client.sendall(payload)
    def __init__(self):
        
        self.ip = "127.0.0.1"
        self.port = 6000
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
                Thread(target=clientThread,args=(client)).start()
            except:
                print("Thread ceration has failed")
                traceback.print_exc()


if __name__ == "__main__":
    #An object of node type is created
    nodo = ServerNode()
    