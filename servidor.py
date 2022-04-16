from socket import socket, AF_INET, SOCK_STREAM
from ssl import SSLContext, PROTOCOL_TLS_SERVER
import string


HOST = "localhost"
PORT = 8005



def make_connection():
    context = SSLContext(PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')

    server = socket(AF_INET, SOCK_STREAM)
    
    server.bind((HOST, PORT))
    server.listen(1)
    tls = context.wrap_socket(server, server_side=True)
    
    connection, address = tls.accept()
    return connection, address

if __name__ == '__main__':

    connection, address = make_connection()
    print(f"Connected by {address}")

    while True:
        data = connection.read(1024)
        print(f'Client Says: {data}')
        print(connection.compression())
        string_ao_contrario = str(data)[::-1]
        connection.sendall(string_ao_contrario.encode("utf-8"))


    ## precisa criar o servidor com o SSL

    # sigilo
    ### mostrar a mensagem que chegou
    ### mostrar a mensagem criptografada

    #Autenticidade
    ### um invasor tenta comunicar com o cliente ou com os servidor e não consegue

    #Sigilo
    ### adiciona qlqr coisa na string e ver que a mensagem criptografada mudou