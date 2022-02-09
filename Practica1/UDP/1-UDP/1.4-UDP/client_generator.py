from client import Client
from sys import argv

""" P1_4 UDP: Generador de clientes. 
    Ejemplo de ejecución del programa por linea de comandos:
    > python client_generator.py SERVER_IP SERVER_PORT CLIENT_ID"""

# Condicion para conocer si se está ejecutando desde el terminal(True) o desde VSC (False)
terminal = len(argv) > 1
if terminal:
    server_ip = argv[1] # Ip del servidor como 1er argumento
    server_port = argv[2] # Puerto del servidor como 2do argumento
    client_id = argv[3] # Ip del cliente como 3er argumento
    try:
        server_port = int(server_port)
        try:
            client_id = int(client_id)
            # Se crea el cliente con el mensaje
            msg = input("[Cliente]: Introduzca un mensaje para enviar al servidor:  ")
            client = Client(client_id)
            client.send_to_server(server_ip,server_port,msg)
            del client
        except:
            print(f"[Cliente]: El id de cliente introducido '{client_id}' no es valido.")
    except:
        print(f"[Cliente]: El puerto '{server_port}' no es valido.")

else:
    # Direccion del servidor
    server_ip = "127.0.0.1"
    #Se pregunta al usuario por el puerto que en el quiere crear el cliente
    while True:
        # Pregunta al usuario el puerto 
        server_port = input("[Cliente]: Indique el puerto al desea conectarse:  ")
        try:
            server_port = int(server_port)
            break
        except:
            print(f"[Cliente]: El puerto {server_port} no es valido")
    # Numero de clientes
    n = 3
    # Se crean clientes recursivamente
    for i in range(0,n):
        # Construccion del mensaje de saludo
        msg = "Hola, soy el cliente " + str(i) 
        client = Client()
        client.send_to_server(server_ip,server_port,msg)
        del client
    # Cliente para cerrar el servidor
    client = Client()
    exit_msg = "EXIT"
    client.send_to_server(server_ip,server_port,exit_msg)