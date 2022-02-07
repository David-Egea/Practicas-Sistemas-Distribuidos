import socket
import pickle
import os
import sys
# Se define el tamaño de MTU
MTU = 1024 # En bytes 
path = sys.path[0]
locks = {}

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
            tx_bytes = []
            try:
                fichero_leido = open(path+"\\files\\"+c_file_name)
                print(fichero_leido)
                # se ha enocntrado el fichero
                tx_bytes = pickle.dumps(fichero_leido.read())
            except :
                # no se ha encontrado el ficher
                error = f"Error 404 File '{c_file_name}' not found."
                print(f"[Server]: {error}")
                tx_bytes = pickle.dumps(error)
            connection.sendall(tx_bytes)
        elif c_instr == "put":
            # Recoge el nombre del fichero a introducir
            c_file_name = c_payload[1]
            # Recoge los datos del fichero
            c_file_data = c_payload[2]
            print(f"[Client]: Put {c_file_name} - {c_file_data}")
            try:
                # Comprueba que el fichero no este bloqueado para el usuario
                authorized = client_address == locks[c_file_name]
                if authorized:
                    # Guarda la entrada
                    fichero = open(f"{path}\\files\\{c_file_name}",'w')
                    fichero.write(c_file_data)
                    payload = f"File '{c_file_name}' saved."
                    print(f"[Server]: {payload}")
                else:
                    payload = f"Unauthorized access to file '{c_file_name}' ."
                    print(f"[Server]: {payload}")
                tx_bytes = pickle.dumps(payload)
                connection.sendall(tx_bytes)
            except KeyError:
                # El archivo no ha sido bloqueado previamente
                error = f"Error 403 Unauthorized access to file '{c_file_name}'."
                print(f"[Server]: {error}")
                tx_bytes = pickle.dumps(error)
                connection.sendall(tx_bytes)
        elif c_instr == "lock":
            # Recoge el nombre del fichero a bloquear
            c_file_name = c_payload[1]
            print(f"[Client]: Lock {c_file_name} for {client_address}")
            # Guarda la entrada
            locks[c_file_name] = client_address
            payload = f"File '{c_file_name}' locked."
            print(f"[Server]: {payload}")
            tx_bytes = pickle.dumps(payload)
            connection.sendall(tx_bytes)
        elif c_instr == "unlock":
            # Recoge el nombre del fichero a introducir
            c_file_name = c_payload[1]
            print(f"[Client]: Unlock {c_file_name}")
            # Guarda la entrada
            locks[c_file_name] = ""
            payload = f"File '{c_file_name}' unlocked."
            print(f"[Server]: {payload}")
            tx_bytes = pickle.dumps(payload)
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