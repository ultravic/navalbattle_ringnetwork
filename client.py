import socket
import sys
import pickle
import navalbattle

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket successfully created'
except:
    print 'Socket creation failed'
    sys.exit()

struct = {
    'id'  : 1,
    'host': socket.gethostname(),
    'port': 5050
}

struct.update({'address': (struct['host'], struct['port'])})

while True:
    message = {
        'host'   : struct['host'],
        'port'   : struct['port'],
        'origin' : '',
        'destiny': '',
        'token'  : ''
    }
    message.update({'data': raw_input('Enter the message: ')})

    try:
        sock.sendto(pickle.dumps(message), (struct['address']))
    except socket.error, message:
        print 'Error code: ' + str(message[0]) + ' Message ' + message[1]
        sys.exit()
