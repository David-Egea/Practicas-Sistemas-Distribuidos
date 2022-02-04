from client import Client
import subprocess

""" P1 UDP: Generador de clientes. """
# Direccion del servidor
server_ip = "127.0.0.1"
#Se pregunta al usuario por el puerto que en el quiere crear el cliente
ok = False
while ok is not True:
    # Pregunta al usuario el puerto 
    server_port = input("[Cliente]: Indique el puerto al desea conectarse:  ")
    try:
        server_port = int(server_port)
        ok = True
    except:
        print(f"[Cliente]: El puerto {server_port} no es valido")
# Se lanza el servidor
#subprocess.Popen
# Numero de clientes
n = 3
# Se crean clientes recursivamente
for i in range(0,n):
    # Construccion del mensaje de saludo
    msg = "Hola, soy el cliente " + str(i) 
    client = Client()
    client.send_to_server(server_ip,server_port,msg)
    del client