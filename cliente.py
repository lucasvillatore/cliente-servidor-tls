from pickle import PROTO
from socket import create_connection
from ssl import SSLContext, PROTOCOL_TLS_CLIENT
from servidor import HOST as HOST_SERVER, PORT as PORT_SERVER

hostname='example.org'



def make_connection():
    context = SSLContext(PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('cert.pem')
    client = create_connection((HOST_SERVER, PORT_SERVER))

    tls = context.wrap_socket(client, server_hostname=hostname)

    return tls
if __name__ == '__main__':

    connection = make_connection()

    while True:
        txt = input("Texto ai brother: ")
        connection.write(txt.encode("utf-8"))
        connection.
        data = connection.recv(1024)
        print(f'Server says: {data}')
    pass