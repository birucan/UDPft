
import socket
import sys

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = "127.0.0.1"
port = 9999
buf =1024
address = (host,port)

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
clientesLlegados=0
data="yes"
while(True):
    print('llego cliente espernado el resto', numClientes-clientesLlegados)
    if(data==sock.recvfrom(1024)):
        data, addr = sock.recvfrom(1024)
    else:
        clientesLlegados=clientesLlegados+1
        data, addr = sock.recvfrom(1024)

    #mensaje="Hola soy el server, te voy a enviar un archivo ome"
    #sender= sock.sendto(mensaje.encode(), addr)
    #data, addr = sock.recvfrom(1024)

    recibido = data
    print("el cliente esta conectado con el mensaje: "+ recibido.decode('ascii'))
    if(numClientes==clientesLlegados):

        f=open(filePath,"rb")
        data = f.read(buf)
        while (data):
            if(sock.sendto(data,address)):
                print ("mandando archivo ...")
                data = f.read(buf)



#f=open(file_name,"rb")
#data = f.read(buf)
#while (data):
#    if(s.sendto(data,address)):
##        data = f.read(buf)
sock.close()
f.close()
