from socket import socket, AF_INET, SOCK_STREAM
import ssl
import string


HOST = "localhost"
PORT = 8001



def make_connection(incoming, outgoing):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')

    server = socket(AF_INET, SOCK_STREAM)
    
    server.bind((HOST, PORT))
    server.listen(1)
    connection, address = server.accept()
    
    tls = context.wrap_bio(incoming, outgoing, server_side=True)
    
    return {"connection": connection, "address": address, "tls": tls}

if __name__ == '__main__':
    tls = {
        "incoming": ssl.MemoryBIO(),
        "outgoing": ssl.MemoryBIO()
    }
    connection_object = make_connection(tls["incoming"], tls["outgoing"])
    print(f"Connected by {connection_object['address']}")

    # while True:
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