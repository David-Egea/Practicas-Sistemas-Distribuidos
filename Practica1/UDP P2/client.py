import socket 
import pickle

from numpy import byte

msg = "Hello"
bytes_tx = pickle.dumps(msg)

server_address = ("127.0.0.1",6700)
socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
socket.sendto(bytes_tx,server_address)

bytes_rx = socket.recvfrom(1024)
message_recieved =pickle.loads(bytes_rx)
print(f"RX: {message_recieved}")
socket.close()
