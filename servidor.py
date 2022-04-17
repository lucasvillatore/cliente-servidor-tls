# authors 
## Lucas Block Villatore - GRR201771677
## Marcus Augusto Ferreira Dudeque - GRR20171616

import ssl
from utils import do_handshake, MESSAGE_SIZE_IN_BYTES, create_context
from socket import socket, AF_INET, SOCK_STREAM

HOST = "localhost"
PORT = 8002

def make_connection(incoming, outgoing):

    tls = create_context(ssl.PROTOCOL_TLS_SERVER, incoming, outgoing, server_side=True)

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    connection, address = server.accept()
    do_handshake(tls, server, incoming, outgoing)


    return {
        'connection': connection,
        'address': address, 
        'tls': tls
    }    

buffers = {
    "incoming": ssl.MemoryBIO(),
    "outgoing": ssl.MemoryBIO()
}

if __name__ == '__main__':
    configuration = make_connection(buffers["incoming"], buffers["outgoing"])
    print(f'Connected by {configuration["address"]}')
    while True:
        pass
    ## precisa criar o servidor com o SSL

    # sigilo
    ### mostrar a mensagem que chegou
    ### mostrar a mensagem criptografada

    #Autenticidade
    ### um invasor tenta comunicar com o cliente ou com os servidor e não consegue

    #Sigilo
    ### adiciona qlqr coisa na string e ver que a mensagem criptografada mudou