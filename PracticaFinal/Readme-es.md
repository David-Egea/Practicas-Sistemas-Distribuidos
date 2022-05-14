# **Middleware para cálculo distribuido**

Autores: 
- Raúl González Gómez
- David Egea Hernández

## Índice

1. Introducción
2. Arquitectura del sistema.

## Introducción
*Esta es la propuesta desarrollada como Práctica Final de la asignatura de Sistemas Distribuidos.*  
El proyecto consiste en la implementación de una red de cálculo sencilla, donde un cliente puede conectarse para enviar tareas soportadas al servicio. 

Los requisitos para levantar la red son:
- Docker instalado
- Soporte para la tarea de nodos

La guía para escribir en [Markdown](https://www.markdownguide.org/basic-syntax/).

## Arquitectura del sistema
La arquitectura empleada en esta ocasión sigue la estructura esclavo-maestro, donde los nodos de procesamiento constituyen los esclavos y hay un único servidor que ejerce de *master* para los *slaves*. Es el nodo maestro quien se encarga de dividir y fragemntar las tareas, enviando los múltiples fragmentos a los distintos nodos de la red atendiendo a la capacidades de procesamiento de cada nodo. 

Un ejemplo

