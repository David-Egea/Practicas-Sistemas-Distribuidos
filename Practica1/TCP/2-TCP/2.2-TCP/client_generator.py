from client import Client

""" P1 UDP: Generador de clientes. """
# Direccion del servidor
server_ip = "127.0.0.1"
server_port = 6780
# Numero de clientes
n = 3
intructions = ["readme.txt","hola.txt","nada"]
# Creacion de un nuevo cliente
client_a = Client()
client_a.send_instr_to_server(instr="get readme.txt")
client_a.send_instr_to_server(instr="bye")
del client_a
# Creacion de un nuevo cliente
client_b = Client()
client_c = Client()
client_b.send_instr_to_server(instr="get nada.txt") # El archivo no existe
client_b.send_instr_to_server(instr="put nada.txt Algo") # No va a estar permitido para el cliente B
client_b.send_instr_to_server(instr="lock nada.txt") # Bloquea para cliente B
client_b.send_instr_to_server(instr="put nada.txt Algo") # Cliente B si tiene permitido guardar
client_b.send_instr_to_server(instr="unlock nada.txt") # Desbloquea el archivo
client_b.send_instr_to_server(instr="get nada.txt") # Se comprueban los cambios guardados por el cliente B
client_b.send_instr_to_server(instr="bye") # Cliente B se despide
del client_b
client_c.send_instr_to_server(instr="lock nada.txt") # Bloquea para cliente C
client_c.send_instr_to_server(instr="put nada.txt Nada_de_nada") # Cliente C ahora tiene permitido guardar
client_c.send_instr_to_server(instr="unlock nada.txt") # Desbloquea el archivo
client_c.send_instr_to_server(instr="get nada.txt") # Se comprueban los cambios guardados por el cliente C
client_c.send_instr_to_server(instr="bye") # Cliente C se despide
del client_c
# Se crean un cliente para cerrar el servidor
client_z = Client()
client_z.send_instr_to_server(instr="exit")
del client_z