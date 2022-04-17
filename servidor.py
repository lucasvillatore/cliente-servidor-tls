# authors 
## Lucas Block Villatore - GRR201771677
## Marcus Augusto Ferreira Dudeque - GRR20171616

from socket import socket, AF_INET, SOCK_STREAM
import ssl

HOST = "localhost"
PORT = 8002

MESSAGE_SIZE_IN_BYTES = 1024

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
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./cert.pem', './key.pem')

    tls = context.wrap_bio(incoming, outgoing, server_side=True)

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
    #     data = connection_object["connection"].recv(MESSAGE_SIZE_IN_BYTES)
    #     if data == 0:
    #         break
    #     tls["incoming"].write(data)
    #     pass
    #     data = connection.read(1024)
    #     print(f'Client Says: {data}')
    #     print(connection.compression())
    #     string_ao_contrario = str(data)[::-1]
    #     connection.sendall(string_ao_contrario.encode("utf-8"))


    ## precisa criar o servidor com o SSL

    # sigilo
    ### mostrar a mensagem que chegou
    ### mostrar a mensagem criptografada

    #Autenticidade
    ### um invasor tenta comunicar com o cliente ou com os servidor e não consegue

    #Sigilo
    ### adiciona qlqr coisa na string e ver que a mensagem criptografada mudou