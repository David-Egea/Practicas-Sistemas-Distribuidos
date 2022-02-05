from client import Client

""" P1 UDP: Generador de clientes. """
# Direccion del servidor
server_ip = "127.0.0.1"
server_port = 6780
# Numero de clientes
n = 2
# Se crean clientes recursivamente
for i in range(0,n):
    # Construccion del mensaje de saludo
    client = Client()
    client.send_msg_to_server("Hi TCP Server, This is a long message that you will received in chunks of 20 bytes")
    del client
# Se crean un cliente para cerrar el servidor
client = Client()
client.send_msg_to_server(msg="EXIT")
del client