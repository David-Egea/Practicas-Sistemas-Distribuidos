from client import Client

""" P1 UDP: Generador de clientes. """
# Direccion del servidor
server_ip = "127.0.0.1"
server_port = 6780

# Se crean clientes
client = Client()
# Construccion del mensaje de saludo
instr = "get " + "nada.txt"
client.send_instr_to_server(instr)
client.send_instr_to_server(instr="bye")

# Se crean clientes
client = Client()
# Construccion del mensaje de saludo
instr = "get " + "hola.txt"
client.send_instr_to_server(instr)
client.send_instr_to_server(instr="bye")

# Se crean un cliente para cerrar el servidor
client = Client()
client.send_instr_to_server(instr="exit")