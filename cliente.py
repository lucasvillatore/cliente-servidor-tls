import ssl
from utils import do_handshake, MESSAGE_SIZE_IN_BYTES
from socket import socket, AF_INET, SOCK_STREAM
from servidor import HOST as HOST_SERVER, PORT as PORT_SERVER

hostname='example.org'
host = "localhost"
port = 2021



def make_connection(incoming, outgoing):
    client = socket(AF_INET, SOCK_STREAM)
    client.bind((host, port))
    client.connect((HOST_SERVER, PORT_SERVER))

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain('./utils/cert.pem', './utils/key.pem')  
    tls = context.wrap_bio(incoming, outgoing, server_hostname=hostname)
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