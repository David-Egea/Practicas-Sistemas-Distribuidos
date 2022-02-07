import socket
import struct
import random
import threading
import pickle

class Client:
    

    def __init__(self) -> None:
        global cerrar
        cerrar = False

        # Client id
        self._id = random.randint(0,65535)
        print(self._id)
        # Multicast 
        self._MCAST_GRP = '224.1.1.1'
        self._MCAST_PORT = 5007

        # socket.AF_INET: Internet Protocol v4 addresses
        # socket.SOCK_DGRAM: UDP datagrams
        # socket.IPPROTO_UDP: set UDP protocol
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind(('',self._MCAST_PORT))
        self.hilo = threading.Thread(target = self.recieve_msg, args=(self.sock,))
        self.hilo.start()
        
        
    def join_group(self, msg: str = "Hola!"):
        # Client message
        msg = f"[Client {self._id}]: {msg}"
        payload = pickle.dumps(msg)
        # Address binding
        self.sock.sendto(payload,(self._MCAST_GRP,self._MCAST_PORT))

        # Tell the operating system to add the socket to the multicast group on all interfaces.
        mreq = struct.pack("4sl",socket.inet_aton(self._MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Setting TTL
        ttl = struct.pack('b',1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def recieve_msg(self,s):
        global cerrar
        
        while cerrar == False:
            # Recieves the message
            payload  = s.recv(1024)
            mensaje_recibido = pickle.loads(payload)
            print(str(self._id)+" "+mensaje_recibido)
            
        s.close()
        print("Hilo terminado")
        
    def send_msg(self, msg: str = "Hola!"):
        # Client message
        payload = pickle.dumps(msg)
        msg = f"[Client {self._id}]: {msg}"
        self.sock.sendto(payload,(self._MCAST_GRP,self._MCAST_PORT))

    def closeConn(self):
        global cerrar
        cerrar = True
        print("Se ha cerrado la conexión")