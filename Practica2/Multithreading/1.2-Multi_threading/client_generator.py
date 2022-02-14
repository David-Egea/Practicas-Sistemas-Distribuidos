from threading import Thread,Lock
import socket


def send_msg_to_server(direccion,msg: str = "Hi TCP Server") -> None:
        global print_lock
        socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_client.connect(direccion)
        """ Envia el mensaje indicado al servidor"""
        print_lock.acquire()
        print(f"[Client]: {msg}")
        print_lock.release()
        socket_client.sendall(msg.encode())
        data = socket_client.recv(1024).decode()
        print_lock.acquire()
        print(f"[Server]: {data}")
        print_lock.release()
        socket_client.close()


if __name__ == "__main__":
    global print_lock
    print_lock = Lock()
    correcto = False

    while correcto==False:
        try:
            puerto = int(input("[Cliente] Introduzca un puerto para levantar el servicio: "))
            direccion = ('127.0.0.1',puerto)
        
            correcto = True
        except:
            print("Introduzca un puerto correcto")
    continuar = True
    #Se crea la lista de mensajes que se van a enviar
    mensajes_clientes = []
    while continuar == True:
        mensaje_enviar = input("[Cliente] Introduzca el mensaje que quiera enviar al servidor: ")
        if mensaje_enviar != "exit":
            mensajes_clientes.append(mensaje_enviar)
        else:
            continuar = False
    #Se recorre la lista de mensajes para enviar
    for mensaje in mensajes_clientes:
        
        Thread(target = send_msg_to_server,args = (direccion,mensaje)).start()
        print("[Cliente] Se está enviando el mensaje '{}'".format(mensaje))

