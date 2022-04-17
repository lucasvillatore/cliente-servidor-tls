import ssl

MESSAGE_SIZE_IN_BYTES = 1024


def create_context(type, incoming, outgoing, **kwargs):
    context = ssl.SSLContext(type)
    context.load_cert_chain('./cert.pem', './key.pem')
    tls = context.wrap_bio(incoming, outgoing, **kwargs)

    return tls

def handle_incoming(socket, incoming):
    print("Incoming")
    try:
        data = socket.recv(MESSAGE_SIZE_IN_BYTES)
        print(data)
    except BaseException as err:
        return 0

    if len(data) == 0: return 0
    return incoming.write(data)

def handle_outgoing(socket, outgoing):
    print("Outgoing")
    data = outgoing.read()
    if len(data) == 0: 
        return
    socket.sendall(data)

def do_handshake(tls, socket, incoming, outgoing):
    isDone = False
    print("Doing handshake")
    # i = 0
    while not isDone:
        try:
            # i += 1
            print("Trying to do handshake")
            tls.do_handshake()
            print("Handshake has been done successfully")
            isDone = True  
        except ssl.SSLWantWriteError:
            print("Write error")
            handle_incoming(socket, incoming)
            handle_outgoing(socket, outgoing)
            
        except ssl.SSLWantReadError:
            print("Read error")
            handle_outgoing(socket, outgoing)
            handle_incoming(socket, incoming)

    handle_outgoing(socket, outgoing)
