import ssl

MESSAGE_SIZE_IN_BYTES = 1024

def do_handshake(tls, socket, incoming, outgoing):
    isDone = False
    print("Doing handshake")
    while not isDone:
        try:
            tls.do_handshake()
            print("Handshake has been done successfully")
            isDone = True  
        except ssl.SSLWantWriteError:
            data = socket.recv(MESSAGE_SIZE_IN_BYTES)
            if len(data) > 0:
                incoming.write(data)
            data = outgoing.read()
            if len(data) > 0:
                socket.send(data)
        except ssl.SSLWantReadError:
            data = outgoing.read()
            print(data)
            if len(data) > 0:
                socket.send(data)
            data = socket.recv(MESSAGE_SIZE_IN_BYTES)
            if len(data) > 0:
                incoming.write(data)
    data = outgoing.read()
    if len(data) > 0:
        socket.send(data)
