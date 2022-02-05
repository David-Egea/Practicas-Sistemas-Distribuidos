import socket
import pickle
import time

""" Servidor Socket TCP """

# Se define el tamaño de MTU
MTU = 1024 # En bytes 

# Se crea el socket del servidor
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Se establece la dirección del servidor
server_address = ("localhost",6780)
# Se vincula el servidor a esa direccion
server_socket.bind(server_address)
server_socket.listen(1)
# El servidor permanece activo 
while True:
    # print("[Server]: Waiting for new client connection...")
    # Se mantiene a la espera hasta aceptar de una conexion con un cliente
    connection,client_address = server_socket.accept()
    # print(f"[Server]: Client connected from address {client_address}")
    # Decodifica los datos recibidos por paquetes
    rx_bytes = connection.recv(MTU)
    client_payload = pickle.loads(rx_bytes)
    # print(f"[Client]: {data} (Full msg)")
    if client_payload == "EXIT":
        # Envia un mensaje de despedida a los clientes conectados
        server_payload = "Bye"
        tx_bytes = pickle.dumps(server_payload)
        connection.sendall(tx_bytes)
        break
    else:
        # Recoge el tiempo del servidor
        server_time = time.time()
        tx_bytes = pickle.dumps(server_time)
        # Envia un saludo a los clientes conectados
        connection.sendall(tx_bytes)
        connection.close()
server_socket.close()
