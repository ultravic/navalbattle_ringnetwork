import socket
import sys
import pickle
import navalbattle
from collections import namedtuple

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket successfully created'
except socket.error, msg:
    print 'Socket creation failed'
    sys.exit()

struct = {
    'id'  : 1,
    'host': socket.gethostname(),
    'port': 5050
}

struct.update({'address': (struct['host'], struct['port'])})

try:
    sock.bind(struct['address'])
    print 'Socket successfully binded at %s' % struct['host']
except socket.error:
    print 'Socket bind failed'
    sys.exit()

while True:
    dataReceiver = sock.recvfrom(4096)
    data = pickle.loads(dataReceiver[0])
    address = dataReceiver[1]

    coord = data['data']
    navalbattle.attackCoord(int(coord[0]), int(coord[1]))

    print 'Message[' + address[0] + ':' + str(address[1]) + ']:'
    print data

sock.close()
