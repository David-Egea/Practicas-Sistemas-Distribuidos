import socket 

msg = "Hello"
bytes_tx = str.encode(msg)

server_address = ("172.24.155.95",6700)
socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
socket.sendto(bytes_tx,server_address)

bytes_rx = socket.recvfrom(1024)
print(f"RX: {bytes_rx}")
socket.close()
