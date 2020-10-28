import socket
import select
import time
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = "127.0.0.1"
port = 9999
buf =1024


sock.bind((host, port))

while (True):
    data, addr = sock.recvfrom(1024)

    if (data):
        print ("File name:", data)
        file_name = "archivo.dummy"

    f = open(file_name, 'wb')
    sock.sendto(data, addr)
    data = (data.decode("ascii")+str((time.time()*1000))).encode("ascii")
    sock.sendto(data, addr)
    while (True):
        ##espera que todos los clientes esten activos
        if(sock.recvfrom(1024)=="ready".encode("ascii")):
            while (True):
                ready = select.select([sock], [], [], 0.2)
                if ready[0]:
                    data, addr = sock.recvfrom(1024)
                    f.write(data)
                else:
                    f.close()
                    break
