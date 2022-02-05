from client import Client

""" P1 UDP: Generador de clientes. """
# Direccion del servidor
server_ip = "127.0.0.1"
server_port = 6780
# Numero de clientes
n = 3
files = ["readme.txt","hola.txt","nada"]
# Se crean clientes recursivamente
for i in range(0,n):
    # Construccion del mensaje de saludo
    client = Client()
    instr = "get " + files[i]
    client.send_instr_to_server(instr)
    client.send_instr_to_server(instr="bye")
# Se crean un cliente para cerrar el servidor
client = Client()
client.send_instr_to_server(instr="exit")