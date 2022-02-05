import socket

# Se define el tamaño de MTU
MTU = 20 # En bytes 

# Se crea el socket del servidor
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Se establece la dirección del servidor
server_address = ("localhost",6780)
# Se vincula el servidor a esa direccion
server_socket.bind(server_address)
server_socket.listen(1)
# El servidor permanece activo 
while True:
    print("[Server]: Waiting for new client connection...")
    # Se mantiene a la espera hasta aceptar de una conexion con un cliente
    connection,client_address = server_socket.accept()
    print(f"[Server]: Client connected from address {client_address}")
    # Decodifica los datos recibidos por paquetes
    p = 0 # Contador de paquetes
    while True:
        p = p + 1 # Incrementa el contador
        data = connection.recv(MTU).decode()
        print(f"[Client]: {data} (Packet {p})")
        if len(data) is not MTU:
            break
    print(f"[Client]: {data} (Full msg)")
    if data == "EXIT":
        # Envia un mensaje de despedida a los clientes conectados
        connection.sendall("Bye".encode())
        break
    else:
        # Envia un saludo a los clientes conectados
        msg = "Hi TCP Client, This is a long message that you will received in chunks of 20 bytes."
        print(f"[Server]: {msg}\n")
        connection.sendall(msg.encode())
        connection.close()
server_socket.close()