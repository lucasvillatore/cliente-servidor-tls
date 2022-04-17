import ssl
from utils import do_handshake, MESSAGE_SIZE_IN_BYTES, create_context
from socket import socket, AF_INET, SOCK_STREAM
from servidor import HOST as HOST_SERVER, PORT as PORT_SERVER

hostname='example.org'
host = "localhost"
port = 20234



def make_connection(incoming, outgoing):
    
    tls = create_context(ssl.PROTOCOL_TLS_CLIENT, incoming, outgoing, server_hostname=hostname)
    
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
    configuration = make_connection(buffers["incoming"], buffers["outgoing"])

    while True:
        pass