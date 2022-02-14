import socket
import sys
import traceback
from threading import Thread

def main():
    start_server()
        
def start_server():
    host = "localhost"
    port = 6780
    # Pregunta la dirección para levantar el servicio
    server_ip = input("[Servidor] Introduzca una dirección IP para levantar el servicio: ")
    # Pregunta el puerto donde levantar dicho servcicio
    while True:
        try:
            server_port = int(input("[Servidor] Introduzca un puerto para levantar el servicio: "))
        except ValueError:
            print("[Servidor] El puerto introducido {} no es un puerto válido: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    try:
        sock.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    sock.listen() 
    # infinite loop- do not reset for every requests
    while True:
        print("Socket now listening")
        connection, address = sock.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connection from client " + ip + ":" + port)
        try:
            Thread(target=clientThread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    sock.close()
    
def clientThread(connection, ip, port, max_buffer_size = 1024):
    is_active = True
    while is_active:
        client_input = connection.recv(max_buffer_size).decode("utf8")
        clientid,msg=client_input.split(":")
        if "quit" in msg:
            print("Client {} is requesting to quit".format(clientid))
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        else:
            print("Client {} sent data: {}".format(clientid,msg))
            connection.send("ok".encode("utf8"))

if __name__ == "__main__":
    main()