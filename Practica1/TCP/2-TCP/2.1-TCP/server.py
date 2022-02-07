import socket
import pickle
import os
import sys

# Se define el tamaño de MTU
MTU = 1024 # En bytes 
path = sys.path[0]
ficheros = os.listdir(path+"\\files")

# Se crea el socket del servidor
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Se establece la dirección del servidor
server_address = ("localhost",6780)
# Se vincula el servidor a esa direccion
server_socket.bind(server_address)
server_socket.listen(1)
# Se enciende el servidor
server_on = True
# El servidor permanece activo 
while server_on:
    print("\n[Server]: Waiting for new client connection...\n")
    # Se mantiene a la espera hasta aceptar de una conexion con un cliente
    connection,client_address = server_socket.accept()
    print(f"[Server]: New client connected from address {client_address}")
    while True:
        # Decodifica los datos recibidos
        rx_bytes = connection.recv(MTU)
        c_payload = pickle.loads(rx_bytes)
        print(f"[Client]: {c_payload}")
        # Divide el payload por espacios
        c_payload = c_payload.split(" ")
        c_instr = c_payload[0] # Instruccion (GET,PUT,BYE..)
        # Intruccion del cliente
        if c_instr == "get":
            # Instruccion get, devuelve un archivo al cliente
            c_file_name = c_payload[1]
            print(f"[Client]: Get {c_file_name}")
            # Se busca el fichero
            tx_bytes = []
            if c_file_name in ficheros:
                try:
                    fichero_leido = open("files/"+c_file_name)
                    
                    # se ha enocntrado el fichero
                    tx_bytes = pickle.dumps(fichero_leido)
                except :
                    # no se ha encontrado el fichero
                    error = f"Error 404 File '{c_file_name}' not found."
                    print(f"[Server]: {error}")
                    tx_bytes = pickle.dumps(error)
            connection.sendall(tx_bytes)
        elif c_instr == "bye":
            # Intruccion para dar por finalizada la comunicacion
            server_bye = "Bye Client."
            print(f"[Server]: {server_bye}.")
            tx_bytes = pickle.dumps(server_bye)
            connection.sendall(tx_bytes)
            print(f"[Server]: Client disconnected from address {client_address}.")
            # Se cierra la connexion con el cliente
            connection.close()
            break
            # connection.close()
        elif c_instr == "exit":
            # Envia un mensaje de despedida a los clientes conectados
            server_close = "Closed server."
            print(f"[Server]: {server_close}.")
            tx_bytes = pickle.dumps(server_close)
            connection.sendall(tx_bytes)
            server_on = False
            break
server_socket.close()