from client import Client

""" P1 UDP: Generador de clientes. """
# Direccion del servidor
server_ip = "127.0.0.1"
server_port = 6700
# Numero de clientes
n = 3
# Se crean clientes recursivamente
for i in range(0,n):
    # Construccion del mensaje de saludo
    msg = "Hola, soy el cliente " + str(i) 
    client = Client()
    client.send_to_server(server_ip,server_port,msg)
    del client