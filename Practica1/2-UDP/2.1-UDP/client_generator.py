from client import Client
from sys import argv

# Condicion para conocer si se está ejecutando desde el terminal(True) o desde VSC (False)
terminal = len(argv) > 1
if terminal:
    server_ip = argv[1] # Ip del servidor como 1er argumento
    server_port = argv[2] # Puerto del servidor como 2do argumento
    client_id = argv[3] # Ip del cliente como 3er argumento
    
    server_port = int(server_port)
    client_id = int(client_id)
    
    # Construccion del mensaje de saludo
    msg = "Hola, soy el cliente {}".format(client_id)
    client = Client()
    client.send_to_server(server_ip,server_port,msg)
    del client
    # Cliente para cerrar el servidor
    client = Client()
    exit_msg = "EXIT"
    client.send_to_server(server_ip,server_port,exit_msg)