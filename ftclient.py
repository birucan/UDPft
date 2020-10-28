import socket
import select
import time
import hashlib

def hash_file(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = "127.0.0.1"
port = 9999
buf =1024

sock.bind((host, port))

while (True):
    data, addr = sock.recvfrom(1024)
    if (data):
        print ("Path:", data)
        file_name = "archivo.dummy"

    f = open(file_name, 'wb')
    sock.sendto(data, addr)
    data = (data.decode("ascii")+str((time.time()*1000))).encode("ascii")

    hash_recibido, addr = sock.recvfrom(1024)
    print("Hash recibido: {}".format(hash_recibido))
    while (True):
        ##espera que todos los clientes esten activos
        ready = select.select([sock], [], [], 3)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        else:
            f.close()
            break
    fin = time.time()
    print('Descarga terminada')
    hash_local = bytes(hash_file("archivo.dummy"),'ascii')
    print("Hash local: {}".format(hash_local))
    if hash_local == hash_recibido:
        print("Hash Correcto - Enviando Recibido")
        sock.sendto("Recibido".encode(),addr)
        inicio, addr = sock.recvfrom(1024)
        print(inicio)
        tiempo = round(fin-float(inicio),2)
        print("Tiempo total: {} segundos".format(tiempo))
        sock.sendto(str(tiempo).encode()+b'\n',addr)
    else:
        print("Error en el Hash")
        sock.sendto("Error de hash".encode(),addr)
        inicio, addr = sock.recvfrom(1024)
        print(inicio)
        tiempo = round(fin-float(inicio),2)
        print("Tiempo total: {} segundos".format(tiempo))
        sock.sendto(str(tiempo).encode()+b'\n',addr)
