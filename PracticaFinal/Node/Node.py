import socket


class Node:
    """ Clase Cliente TCP """

    def __init__(self, server_address: tuple = ("localhost",6780)) -> None:
        self.server_address = server_address
        
    # def __del__(self) -> None:
        # # Se cierra el socket del cliente
        # self.socket_client.close()

    def send_msg_to_server(self, msg: str = "Hi TCP Server") -> None:
        global print_lock
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(self.server_address)
        """ Envia el mensaje indicado al servidor"""
        print_lock.acquire()
        print(f"[Client]: {msg}")
        print_lock.release()
        self.socket_client.sendall(msg.encode())
        data = self.socket_client.recv(1024).decode()
        print_lock.acquire()
        print(f"[Server]: {data}")
        print_lock.release()
        self.socket_client.close()