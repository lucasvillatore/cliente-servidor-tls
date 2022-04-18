# authors 
## Lucas Block Villatore - GRR201771677
## Marcus Augusto Ferreira Dudeque - GRR20171616

# Ultima modificação - 17/04/2022

import ssl
from utils import do_handshake, MESSAGE_SIZE_IN_BYTES, treat_buffer_read_message, treat_buffer_write_message
from socket import socket, AF_INET, SOCK_STREAM

HOST = "localhost"
PORT = 8011

def make_connection(incoming, outgoing):

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="./cert.pem", keyfile="./key.pem")
    tls = context.wrap_bio(incoming, outgoing, server_side=True)

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server up on port {PORT}")
    print("Waiting for client connect")

    connection, address = server.accept()
    connection.setblocking(False)

    print("Connected by {}".format(address))

    do_handshake(tls, connection, incoming, outgoing)

    return {
        'connection': connection,
        'address': address, 
        'tls': tls
    }    


def recv(configuration, buffers):
    while True:
        try:
            return configuration["tls"].read(MESSAGE_SIZE_IN_BYTES)
        except ssl.SSLWantReadError:
            treat_buffer_read_message(configuration["connection"], buffers["incoming"])

def send(message, buffers, configuration):
    configuration["tls"].write(message)
    treat_buffer_write_message(configuration["connection"], buffers["outgoing"])
           
buffers = {
    "incoming": ssl.MemoryBIO(),
    "outgoing": ssl.MemoryBIO()
}

if __name__ == '__main__':
    configuration = make_connection(buffers["incoming"], buffers["outgoing"])
    while True:
        message = recv(configuration, buffers).decode("utf-8")
        print("Message received from client: {}".format(message))
        send(message[::-1].encode("utf-8"), buffers, configuration)

