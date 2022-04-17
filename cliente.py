import os
from socket import socket, AF_INET, SOCK_STREAM
import ssl
from servidor import HOST as HOST_SERVER, PORT as PORT_SERVER, MESSAGE_SIZE_IN_BYTES

hostname='example.org'
host = "localhost"
port = 2021

def do_handshake(tls, server, incoming, outgoing):
    isDone = False
    print("Doing handshake")
    while not isDone:
        try:
            tls.do_handshake()
            print("Handshake has been done successfully")
            isDone = True  
        except ssl.SSLWantWriteError:
            data = server.recv(MESSAGE_SIZE_IN_BYTES)
            if len(data) > 0:
                incoming.write(data)
            data = outgoing.read()
            if len(data) > 0:
                server.send(data)
        except ssl.SSLWantReadError:
            data = outgoing.read()
            print(data)
            if len(data) > 0:
                server.send(data)
            data = server.recv(MESSAGE_SIZE_IN_BYTES)
            if len(data) > 0:
                incoming.write(data)
    data = outgoing.read()
    if len(data) > 0:
        server.send(data)


def make_connection(incoming, outgoing):
    client = socket(AF_INET, SOCK_STREAM)
    client.bind((host, port))
    client.connect((HOST_SERVER, PORT_SERVER))

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain('./cert.pem', './key.pem')  
    tls = context.wrap_bio(incoming, outgoing, server_hostname=hostname)
    do_handshake(tls, client, incoming, outgoing)
    print('chego aqui')
    return {
        "client": client,
        "tls": tls
    }

buffers = {
    "incoming": ssl.MemoryBIO(),
    "outgoing": ssl.MemoryBIO()
}

if __name__ == '__main__':
    configuration = make_connection(buffers["incoming"], buffers["outgoing"])

    while True:
        pass
    #     connection_object["tls"].write(b"oi")
    #     data = tls["outgoing"].read()
    #     print(len(data))
    #     connection_object["client"].sendall(data)
    #     pass
    #     txt = input("Texto ai brother: ")
    #     connection.write(txt.encode("utf-8"))
    #     connection.
    #     data = connection.recv(1024)
    #     print(f'Server says: {data}')
    # pass