import socket 
import pickle

msg = "Hello"
bytes_tx = pickle.dumps(msg)

server_address = ("127.0.0.1",6700)
socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
socket.sendto(bytes_tx,server_address)

bytes_rx = socket.recvfrom(1024)
print(f"RX: {bytes_rx}")
socket.close()
