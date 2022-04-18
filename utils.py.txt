# authors 
## Lucas Block Villatore - GRR201771677
## Marcus Augusto Ferreira Dudeque - GRR20171616

# Ultima modificação - 17/04/2022


import ssl

MESSAGE_SIZE_IN_BYTES = 1024

def treat_buffer_read_message(socket, incoming):
    try:
        data = socket.recv(MESSAGE_SIZE_IN_BYTES)
    except Exception as err:
        data = 0

    if data != 0:
        return incoming.write(data)
    return data

def treat_buffer_write_message(socket, outgoing):
    data = outgoing.read()
    if len(data) == 0: return
    socket.sendall(data)

    return data


def do_handshake(tls, socket, incoming, outgoing):
    isDone = False
    print("Doing handshake")
    while not isDone:
        try:
            tls.do_handshake()
            print("Handshake has been done successfully")
            isDone = True  
        except ssl.SSLWantWriteError:
            treat_buffer_read_message(socket, incoming)
            treat_buffer_write_message(socket, outgoing)
            
        except ssl.SSLWantReadError:
            treat_buffer_write_message(socket, outgoing)
            treat_buffer_read_message(socket, incoming)

    treat_buffer_write_message(socket, outgoing)
