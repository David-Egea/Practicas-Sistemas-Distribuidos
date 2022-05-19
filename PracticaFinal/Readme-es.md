# **Middleware para cálculo distribuido**

Autores: 
- Raúl González Gómez
- David Egea Hernández
___
## Índice

1. Introducción
2. Arquitectura del sistema.
3. Caso de uso
___
## 1. Introducción
*Esta es la propuesta desarrollada como Práctica Final de la asignatura de Sistemas Distribuidos.*  
El proyecto consiste en la implementación de un servicio de cálculo distribuido, donde un cliente puede enviar una serie tareas que son procesadas por los diferentes nodos que conforman la red de computación. 

![La imagen no se encuentra disponible :(](concept.svg "Concepto de servicio")
___
## 2. Arquitectura del sistema

La arquitectura empleada en esta ocasión sigue la estructura esclavo-maestro, donde los nodos de procesamiento constituyen los esclavos y hay un único servidor que ejerce de *master* para los *slaves*. Es el nodo maestro quien se encarga de dividir y fragemntar las tareas, enviando los múltiples fragmentos a los distintos nodos de la red atendiendo a la capacidades de procesamiento de cada nodo. 

___
## 2.1. Esquema de funcionamiento
A continuación se muestra un ejemplo del funcionamiento del sistema de cálculo distribuido, para la siguiente situación:

*Un cliente desea enviar dos tareas distintas al DCN (Distributed Computing Network), cada una está includida en las requests correspondientes A y B.*

![La imagen no se encuentra disponible :(](diagram-es.svg "Concepto de servicio")
___
## 3. Guía práctica.

### 3.0. Pre-requisitos
*`[Atención]: En caso de no cumplir con los criterios necesarios para el despliege de los nodos necesarios, no será posible poner en práctica la red de cálculo distribuido.`*

Antes de comenzar con la instalación, **es necesario contar con una serie de requisitos**, en función del tipo de nodo que se desee instalar.

Para desplegar un nodo cliente o ***client node*** es necesario cumplir con las siguientes condiciones: 
- Contar con [Docker](https://www.docker.com/) instalado en el dispositivo.
- Contar con [WinSCP](https://winscp.net/eng/index.php?) instalado en el dispositivo.

Para desplegar un nodo servidor o ***server node*** es necesario cumplir con las siguientes condiciones: 
- Contar con [Docker](https://www.docker.com/) instalado en el dispositivo.

Para desplegar un nodo de procesamiento o ***slave node*** es necesario cumplir con las siguientes condiciones: 
- Contar con [Docker](https://www.docker.com/) instalado en el dispositivo.

### 3.1 Preparación de los nodos
*`[Atención]: El order de activación es crítico. No levantar los nodos siguiendo las intrucciones incluidas a continuación puede provocar el fallo del sistema.`*

Primeramente, se deberá levantar el nodo servidor. El *server node* debe ser **siempre** el primer elemento en activarse. De lo contrario, la conexión con el resto de nodos de la red no será posible. Para generar una imagen *Docker* del *server*, se deberá ir al directorio **.../PracticaFinal/server_files**, donde se deberá localizar el fichero *Dockerfile*.

A continuación se deberá de abrir un terminal y ejecutar el siguiente comando:
```
docker build -t server.
````

Tras haber generado la imagen deseada, se deberá poner a correr un contenedor:
````
docker run -it -d --network host --name server server
````

Una vez activado el servidor, es el turno de los *slave nodes*. De igual forma, se deberá acceder a la carpeta **.../PracticaFinal/slave_files**, donde se deberá localizar el fichero *Dockerfile*, que en este caso corresponde al esclavo. Siguiendo el mismo procedimiento que anteriormente para generar la imagen:
```
docker build -t slave .
```

Para ejecutar el contenedor del nodo de procesamiento:
```
docker run -it -d --network host --name slave slave
```

Por último, es el turno del *client node*. Se deberán ejecutar los siguientes comandos:
```
docker build -t client .
```
```
docker run -it -d --network host --name client client
```

Para comprobar si efectivamente todos los nodos se han levantado correctamente, se deberá obtener una captura similar a esta, donde poder apreciar los contenedores en ejecución que han sido creados.

![La imagen no se encuentra disponible :(](containers.png "[Portainer] Running containers.")

### 3.2 Enviar archivos usando FTP

FTP es un protocolo de transferencia que permite enviar archivos entre dispositivos conectados a una misma red TCP. En el caso de esta práctica, se ha empleando la aplicación [WinSCP](https://winscp.net/eng/index.php?) para enviar imágenes desde el pc del cliente al nodo del mismo que se encuentra en el contenedor. Estas imágenes serán enviadas al *server nodo* y posteriormente procesadas según lo indicado en el **Apartado 3**. 

![La imagen no se encuentra disponible :(](winscp_show.png "[WinSCP] Ejemplo de uso.")

De esta forma, el cliente es capaz de enviar y recibir las imágenes a través de una sencilla interfaz.

**`Importante`**: La configuración de la herramienta deberá realizarse según se indica en la siguiente captura.

![La imagen no se encuentra disponible :(](winscp_log.png "[WinSCP] Iniciar sesión.")

En primer lugar el protocolo deberá establecerse en **FTP**, no se debe incluir cifrado, la dirección del servidor se ajustará a **192.168.1.7**, el puerto que se utilizará es el *2121*. Por otro lado, las credenciales de acceso son, **usuario** y la contraseña, **usuario**. A continuación se deberá pulsar el botón de **conectar**.

Una vez realizado este proceso, se le mostrarán una interfaz con dos *boxes* principales. La *box* de la izquierda muestra el contenido de la carpeta local, y se deberá acceder al directorio del cual descuelgen las imágenes que se deseen procesar. La *box* de la derecha por el contrario, deberá mostrar la carpeta *filesToDo*, que es el buzón de entrada. Para procesar las imágenes, se deberán arrastar de la primera *box* a la segunda. 

### 3.3 Ejemplo de uso

Por último, se muestra un ejemplo de uso de esta red de cálculo. En este caso el funcionamiento de los nodos es bien sencillo, se limita a procesar imágenes a color y convertirlas a escala de grises. 

A continuación se muestra un ejemplo realizado utilizando este sistema desarrollado:

Imagen Original           |  Imagen Procesada
:-------------------------:|:-------------------------:
![La imagen no se encuentra disponible :(](example.jpg "[WinSCP] Imagen original.")  |  ![La imagen no se encuentra disponible :(](example_processed.jpg "[WinSCP] Imagen procesada.")
---
## 4. Futuras mejoras

Actualmente, esta primera versión de sistema cuenta con algunas limitaciones observadas durante el proceso de desarrollo:

- Las direcciones de los nodos se encuentran fijadas en los archivos de configuración, por lo que la asignación de la IP de red y el puerto no se realiza de forma automática. 
- La funcionalidad soportada por los nodos es limitada, y depende fundamentalmente de los módulos de procesamiento incorporados. Esto obliga a desarrollar esto como una clase . La idea es perfilar esta característica para adaptarla a una arquitectura orientada a microservicios. Desacoplando de esta forma el nodo cliente de la implementación del procesamiento. 
- La red contendores docker es de tipo *host* y funciona perfectamente en el caso de que todos los nodos se encuentran dentro de la misma máquina. No obstante, para una implementación orientada a una arquitectura distribuida, sería más conveniente apostar por su despligue en redes de tipo *overlay*. 