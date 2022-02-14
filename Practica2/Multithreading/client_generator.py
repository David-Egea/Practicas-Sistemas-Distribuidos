from client import Client

""" P1 UDP: Generador de clientes. """

correcto = False

while correcto==False:
    try:
        puerto = int(input("Introduzca un número de puerto"))
        direccion = ('localhost',puerto)
        # Construccion del mensaje de saludo
        client = Client(direccion)
        correcto = True
    except:
        print("Introduzca un puerto correcto")

# Se crean un cliente para cerrar el servidor
client = Client()
client.send_msg_to_server(msg="EXIT")
del client