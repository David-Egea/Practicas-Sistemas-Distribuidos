from client import Client
import time

""" P1 UDP: Generador de clientes. """
# Direccion del servidor
server_ip = "127.0.0.1"
server_port = 6780
# Numero de clientes
n = 100000
diff_time = 0
start_time = time.time()
print(f"Starting {n} TCP calls")
# Se crean clientes recursivamente
for i in range(0,n):
    # Construccion del mensaje de saludo
    client = Client()
    diff_time =  diff_time + client.get_server_time()
# Se hace el calculo del tiempo transcurrido
elapsed_time = time.time() - start_time
print(f"[Elapsed Time]: {elapsed_time} (s) for {n} tcp calls")
# Se crean un cliente para cerrar el servidor
client = Client()
client.send_msg_to_server(msg="EXIT")
# Se muestran los datos
avg_diff_time = diff_time/100000
# Se muestra el tiempo medio de diferencia
print(f"[Average Difference Time]: {avg_diff_time} (s)")