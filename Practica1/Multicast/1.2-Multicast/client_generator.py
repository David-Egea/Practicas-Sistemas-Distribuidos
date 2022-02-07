from client import Client

#Se crea el cliente
cliente = Client()
# Se le añade al grupo
cliente.join_group()

#Flag para que se quede en bucle
terminar = False
while terminar == False:
    mensaje = str(input("Escriba el mensaje que desea enviar\n"))
    if mensaje == "Quit":
        cliente.closeConn()
        terminar = True
    else:
        cliente.send_msg(mensaje)
