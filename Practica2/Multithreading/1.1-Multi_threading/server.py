import socket
import sys
from threading import Thread
import traceback

def main():
    start_server()
        
def start_server():
    # Pregunta la dirección para levantar el servicio
    # server_ip = input("[Servidor] Introduzca una dirección IP para levantar el servicio: ")
    server_ip = "127.0.0.1"
    # Pregunta el puerto hasta que se introduce uno valido
    while True:
        # Pregunta el puerto donde levantar dicho servcicio
        port = input("[Servidor] Introduzca un puerto para levantar el servicio: ")
        try:
            # Se convierte la cadena de caracteres a un entero
            server_port = int(port)
            break
        except ValueError:
            print(f"[Servidor] El puerto introducido '{port}' no es un puerto válido.\n")
    # Se crea el socket del servidor 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("[Servidor] El servidor se ha creado correctamente.")
    try:
        # Server binding
        server_socket.bind((server_ip,server_port))
    except:
        print(f"[Servidor] Ha fallado la asignación de la dirección al servidor. ({sys.exc_info()})")
        sys.exit()
    # El servidor se mantiene a la espera 
    server_socket.listen() 
    # infinite loop- do not reset for every requests
    while True:
        print("[Servidor] El servidor está a la escucha...")
        # Espera conexiones de clientes
        client, (ip, port) = server_socket.accept()
        print(f"[Servidor] Se ha conectado un cliente en la dirección {ip} con puerto {port}.")
        try:
            Thread(target=clientThread,args=(client,1024)).start()
        except:
            print("[Servidor] Ha fallado la creación del Thread!")
            traceback.print_exc()
    
def clientThread(client, max_buffer_size = 1024):
    # El mensaje enviado por el cliente
    msg = client.recv(max_buffer_size).decode("utf8")
    print(f"[Cliente]: {msg}")
    # Se envía el mensaje enviado al cliente de vuelta a modo de confirmación
    client.sendall(msg.encode())

if __name__ == "__main__":
    main()