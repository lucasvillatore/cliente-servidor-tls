# authors 
## Lucas Block Villatore - GRR201771677
## Marcus Augusto Ferreira Dudeque - GRR20171616

# Ultima modificação - 17/04/2022


import ssl
from utils import do_handshake, MESSAGE_SIZE_IN_BYTES, treat_buffer_read_message, treat_buffer_write_message
from socket import socket, AF_INET, SOCK_STREAM
from servidor import HOST as HOST_SERVER, PORT as PORT_SERVER

hostname='example.org'
host = "localhost"
port = 20234



def make_connection(incoming, outgoing):
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain(certfile="./cert.pem", keyfile="./key.pem")
    context.load_verify_locations("./cert.pem")
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

def send(message, buffers, configuration):
    print("Sending message to server\n")
    message = message.encode("utf-8")
    configuration["tls"].write(message)
    return treat_buffer_write_message(configuration["client"], buffers["outgoing"])
    

def recv(configuration, buffers):
    print("Receiving message from server\n")
    while True:
        try:
            return configuration["tls"].read(MESSAGE_SIZE_IN_BYTES)
        except ssl.SSLWantReadError:
            treat_buffer_read_message(configuration["client"], buffers["incoming"])

if __name__ == '__main__':
    configuration = make_connection(buffers["incoming"], buffers["outgoing"])

    while True:
        text = input("Digite sua string maluca: ")
        
        print("--------- SIGILO ---------\n")
        
        mensagem_criptografada = send(text, buffers, configuration)
        mensagem = recv(configuration, buffers)
        
        print("Mensagem descriptografada: " + str(text))
        print("Mensagem criptografada: " + str(mensagem_criptografada))
        print("Mensagem do servidor: " + mensagem.decode("utf-8"))
        print("--------- SIGILO ---------\n")
        
        print()
        print("--------- INTEGRIDADE ---------\n")
        
        mensagem_original_modificada_criptografada = send(text + " STRING ALEATORIA NO FINAL", buffers, configuration)
        mensagem = recv(configuration, buffers)
        
        print("Mensagem criptografada original: " + str(mensagem_criptografada))
        print("Mensagem criptografada modificada: " + str(mensagem_original_modificada_criptografada))
        print("Mensagem do servidor com a mensagem modificada: ", mensagem)
        
        print("--------- INTEGRIDADE ---------\n")