from client import Client
import time

# Creacion de clientes
print("Client A")
client_a = Client()
print("Client B")
client_b = Client()
print("Client C")
client_c = Client()

#Nadie va a mostrar el mensaje de a, puesto que es el primero en meterse en el grupo
client_a.join_group()
client_b.join_group()
client_c.join_group()

#Se manda un mensaje desde a
mensaje_a = "Todo va ok"
client_a.send_msg(mensaje_a)

#Se manda un mensaje desde b
mensaje_b = "Todo va ok"
client_b.send_msg(mensaje_b)

input()
#Se cierra la conexion
adios = "Adios"
client_b.send_msg(adios)

