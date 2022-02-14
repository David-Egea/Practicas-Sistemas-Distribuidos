import socket


class Client:
    """ Clase Cliente TCP """

    def __init__(self, server_address: tuple = ("localhost",6780)) -> None:
        self.server_address = server_address

    def send_msg_to_server(self, msg: str = "Hi TCP Server") -> None:
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect(self.server_address)
        """ Envia el mensaje indicado al servidor"""
        print(f"[Client]: {msg}")
        self.socket_client.sendall(msg.encode())
        data = self.socket_client.recv(1024).decode()
        print(f"[Server]: {data}")
        self.socket_client.close()