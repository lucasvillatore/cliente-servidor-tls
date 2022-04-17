# authors 
## Lucas Block Villatore - GRR201771677
## Marcus Augusto Ferreira Dudeque - GRR20171616

# Ultima modificação - 17/04/2022


import ssl
from utils import do_handshake
from socket import socket, AF_INET, SOCK_STREAM
from servidor import HOST as HOST_SERVER, PORT as PORT_SERVER

hostname='example.org'
host = "localhost"
port = 20234



def make_connection(incoming, outgoing):
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls = context.wrap_bio(incoming, outgoing, server_hostname=hostname)

    client = socket(AF_INET, SOCK_STREAM)

    print("Connecting on server")   
    client.connect((HOST_SERVER, PORT_SERVER))
    client.setblocking(False)
    
    do_handshake(tls, client, incoming, outgoing)

    return {
        "client": client,
        "tls": tls
    }

buffers = {
    "incoming": ssl.MemoryBIO(),
    "outgoing": ssl.MemoryBIO()
}

if __name__ == '__main__':
    try:
        configuration = make_connection(buffers["incoming"], buffers["outgoing"])
    except Exception as err:
        print("Erro ao tentar conectar ao servidor")
        print("message: {}".format(str(err)))