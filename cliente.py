from pickle import PROTO
from socket import create_connection
import ssl
from servidor import HOST as HOST_SERVER, PORT as PORT_SERVER

hostname='example.org'



def make_connection(tls):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('cert.pem')
    client = create_connection((HOST_SERVER, PORT_SERVER))

    tls = context.wrap_bio(tls["incoming"], tls["outgoing"], server_hostname=hostname)
    return tls

tls = {
    "incomming": ssl.MemoryBIO(),
    "outgoing": ssl.MemoryBIO()
}
if __name__ == '__main__':

    connection_object = make_connection(tls)

    # while True:
    #     txt = input("Texto ai brother: ")
    #     connection.write(txt.encode("utf-8"))
    #     connection.
    #     data = connection.recv(1024)
    #     print(f'Server says: {data}')
    # pass