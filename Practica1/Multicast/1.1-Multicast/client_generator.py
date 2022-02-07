from client import Client
import time

# Creacion de clientes
client_a = Client()
client_a.join_group()
client_b = Client()
client_b.join_group()
client_c = Client()
client_c.join_group()

#Se manda un mensaje desde a
mensaje_a = "Todo va ok"
client_a.send_msg(mensaje_a)


#Se manda un mensaje desde b
mensaje_b = "Todo va ok"
client_b.send_msg(mensaje_b)


#Se cierra la conexion
adios = "Adios"
client_b.send_msg(adios)

