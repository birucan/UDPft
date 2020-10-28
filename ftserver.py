
import socket
import sys
import threading
import ntpath
import os
import hashlib
import time
import queue
from datetime import datetime

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = "127.0.0.1"
port = 9999
buf =1024
address = (host,port)
fecha = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

print("Archivos:")
print(" (1) 1.dummy -   100mb")
print(" (2) 2.dummy -   250mb")
print("----------------")
foo = int(input("Archivo a enviar (1 o 2): "))
if(foo==1):
    filePath = './archivos/1.dummy'
if(foo==2):
    filePath = './archivos/2.dummy'

numClientes = int(input("Ingrese numero de clientes: "))
sock.sendto(filePath.encode('ascii'),address)

def hash_file(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

while(True):
    data, addr = sock.recvfrom(1024)
        #mensaje="Hola soy el server, te voy a enviar un archivo ome"
        #sender= sock.sendto(mensaje.encode(), addr)
        #data, addr = sock.recvfrom(1024)

    filename = path_leaf(filePath)
    filesize = f'{os.path.getsize(filePath)}'


    recibido = data
    print("el cliente esta conectado con el mensaje: "+ recibido.decode('ascii'))
    sock.sendto(hash_file(filePath).encode(),address)

    log = fecha + " | " + filename + " | " + str(round((int(filesize)/1024),2)) + "KB"
    inicio = time.time()
    
    f=open(filePath,"rb")
    data = f.read(buf)
    while (data):
        if(sock.sendto(data,address)):
            print ("mandando archivo ...")
            data = f.read(buf)
    print("transferencia terminada")
    client_recibido = sock.recv(buf).decode()
    
    if client_recibido == "Recibido":
        print("Enviado con exito a cliente")
        sock.sendto(str(inicio).encode(),address)
        tiempo = float(sock.recv(buf).decode())
        log = log + " | Tiempo: " + str(tiempo) + "s | Exitoso\n"
    else:
        print("Errores en el envio a cliente")
        print(str(inicio).encode())
        sock.sendto(str(inicio),address)
        tiempo = float(sock.recv(buf).decode())
        log = log + " | Tiempo: " + str(tiempo) + "s | Error\n"

    log_file = open(fecha+".txt",'a')
    log_file.write(log)
    log_file.close()
sock.close()
f.close()