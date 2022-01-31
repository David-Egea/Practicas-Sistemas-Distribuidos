import socket


i = 1

socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
socket.bind(("127.0.0.1",6700))


while True:
    
    bytes_rx = socket.recvfrom(1024)
    message = bytes_rx[0]
    address = bytes_rx[1]
    print(message)

    msg = "Hello Client {}".format(i)
    i +=1
    bytes_tx = str.encode(msg)
    socket.sendto(bytes_tx,address)