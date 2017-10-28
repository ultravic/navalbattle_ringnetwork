import math
import socket
import sys
import pickle

def init(N, S):
    global tableN, tableSize, table, numberShips
    tableN = N
    tableSize = N * N
    table = range(0, tableSize)
    for i in range(0, tableSize):
        table[i] = 0
    maxShips = math.floor(tableSize/6)
    numberShips = maxShips if S > maxShips else S

def addShip(line, column, type, s):
    if type.upper() == 'L':
        if column < 4:
            if (table[(line-1)*tableN + column-1] == 0 and
            table[(line-1)*tableN + column] == 0 and
            table[(line-1)*tableN + column+1] == 0):
                table[(line-1)*tableN + column-1] = s
                table[(line-1)*tableN + column] = s
                table[(line-1)*tableN + column+1] = s
            else:
                print "Ja existe um navio nessas coordenadas"
                return 0
        else:
            print "Coordenadas fora dos limites 1x3"
    elif type.upper() == 'C':
        if line < 4:
            if (table[(line-1)*tableN + column-1] == 0 and
            table[line*tableN + column-1] == 0 and
            table[(line+1)*tableN + column-1] == 0):
                table[(line-1)*tableN + column-1] = s
                table[line*tableN + column-1] = s
                table[(line+1)*tableN + column-1] = s
            else:
                print "Ja existe um navio nessas coordenadas"
                return 0
        else:
            print "Coordenadas fora dos limites 3x1"
    else:
        print "Tipo inexistente"
        return 0
    return 1

def attackCoord(line, column):
    global numberShips, tableN, table
    line -= 1
    column -= 1
    if line > (tableN-1) or line < 0 or column > (tableN-1) or column < 0:
        print "Coordenadas fora do tabuleiro"
        return 0
    else:
        if line == 1:
            if column == 1:
                if table[line*tableN + column] != 0:
                    if (table[line*tableN + column+1] == 0 and
                    table[(line+1)*tableN + column] == 0):
                        print "Navio %d destruido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    elif table[line*tableN + column] != 0:
                        print "Navio %d atingido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                else:
                    print "Missil atingiu a agua"
            elif column == tableN:
                if table[line*tableN + column] != 0:
                    if (table[line*tableN + column-1] == 0 and
                    table[(line+1)*tableN + column] == 0):
                        print "Navio %d destruido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    elif table[line*tableN + column] != 0:
                        print "Navio %d atingido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                else:
                    print "Missil atingiu a agua"
            else:
                if table[line*tableN + column] != 0:
                    if (table[line*tableN + column+1] == 0 and
                    table[line*tableN + column-1] == 0 and
                    table[(line+1)*tableN + column] == 0):
                        print "Navio %d destruido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    elif table[line*tableN + column] != 0:
                        print "Navio %d atingido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                else:
                    print "Missil atingiu a agua"
        elif line == tableN:
            if column == 1:
                if table[line*tableN + column] != 0:
                    if (table[line*tableN + column+1] == 0 and
                    table[(line-1)*tableN + column] == 0):
                        print "Navio %d destruido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    elif table[line*tableN + column] != 0:
                        print "Navio %d atingido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                else:
                    print "Missil atingiu a agua"
            elif column == tableN:
                if table[line*tableN + column] != 0:
                    if (table[line*tableN + column-1] == 0 and
                    table[(line-1)*tableN + column] == 0):
                        print "Navio %d destruido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    elif table[line*tableN + column] != 0:
                        print "Navio %d atingido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                else:
                    print "Missil atingiu a agua"
            else:
                if table[line*tableN + column] != 0:
                    if (table[line*tableN + column+1] == 0 and
                    table[line*tableN + column-1] == 0 and
                    table[(line-1)*tableN + column] == 0):
                        print "Navio %d destruido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    elif table[line*tableN + column] != 0:
                        print "Navio %d atingido" % table[line*tableN + column]
                        table[line*tableN + column] = 0
                else:
                    print "Missil atingiu a agua"
        else:
            if table[line*tableN + column] != 0:
                if (table[line*tableN + column+1] == 0 and
                table[line*tableN + column-1] == 0 and
                table[(line-1)*tableN + column] == 0 and
                table[(line+1)*tableN + column] == 0):
                    print "Navio %d destruido" % table[line*tableN + column]
                    table[line*tableN + column] = 0
                    numberShips -= 1
                elif table[line*tableN + column] != 0:
                    print "Navio %d atingido" % table[line*tableN + column]
                    table[line*tableN + column] = 0
            else:
                print "Missil atingiu a agua"
    return 1

def printTable():
    global tableN, table
    for i in range(0, tableN):
        print ' '.join(str(x) for x in table[i*tableN:i*tableN+tableN])

def connection():
    global sock, struct_server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Socket successfully created'
    except:
        print 'Socket creation failed'
        sys.exit()

    struct_server = {
        'id'       : 1,
        'host'     : socket.gethostname(),
        'port'     : 5050,
        'has_token': True,
        'next'     : ''
    }

    struct_server.update({'address': (struct_server['host'], struct_server['port'])})

    try:
        sock.bind(struct_server['address'])
        print 'Socket successfully binded at %s' % struct_server['host']
    except socket.error:
        print 'Socket bind failed'
        sys.exit()

def play():
    connection()

    n = int(raw_input("Tamanho do tabulerio : "))
    s = int(raw_input("Quantidade de navios : "))

    init(n, s)

    while s:
        coordenations = raw_input("Coordenadas e tipo(linha,coluna,tipo): ")
        coordenations = coordenations.split(',')
        if len(coordenations) != 3:
            print "Devem haver necessariamente 2 coordenadas e 1 tipo. Digite novamente"
            continue
        validate = addShip(int(coordenations[0]), int(coordenations[1]), coordenations[2], s)
        if validate:
            s -= 1

    printTable()

    while numberShips:
        if struct_server['has_token']:
            print "É a sua vez!"
            message = {
                'id'       : struct_server['id']
                'host'     : struct_server['host'],
                'port'     : struct_server['port'],
                'origin'   : struct_server['address'],
                'destiny'  : '',
                'type'     : 'A',
                'has_token': False,
                'received' : 0
            }

            player = int(raw_input("Escolha um jogador(1-4): "))
            while player == struct_server['id']:
                print 'Ataque alguém que não seja você!'
                player = int(raw_input("Escolha um jogador(1-4): "))


            coordenations = raw_input("Coordenadas de ataque (linha,coluna): ")
            coordenations = coordenations.split(',')
            while len(coordenations) != 2:
                print "Devem haver necessariamente 2 coordenadas. Digite novamente"
                coordenations = raw_input("Coordenadas de ataque (linha,coluna): ")
                coordenations = coordenations.split(',')

            message.update({'data': coordenations})

            try:
                sock.sendto(pickle.dumps(message), (struct_server['address']))
            except socket.error, message:
                print 'Error code: ' + str(message[0]) + ' Message ' + message[1]
                sys.exit()

            dataReceiver = sock.recvfrom(4096)

            message = {
                'id'       : struct_server['id']
                'host'     : struct_server['host'],
                'port'     : struct_server['port'],
                'origin'   : struct_server['address'],
                'destiny'  : '',
                'type'     : 'A',
                'has_token': True,
                'received' : 0
            }

            try:
                sock.sendto(pickle.dumps(message), (struct_server['address']))
            except socket.error, message:
                print 'Error code: ' + str(message[0]) + ' Message ' + message[1]
                sys.exit()

        else:
            print 'Aguardando jogadores...'
            while not struct_server['has_token']:
                dataReceiver = sock.recvfrom(4096)
                data = pickle.loads(dataReceiver[0])
                address = dataReceiver[1]

                if data['destiny'] == struct_server['address']
                    data['received'] = 1
                    response = attackCoord(int(data['data'][0]), int(data['data'][1]))

                elif data['type'] == 'D':
                    print 'Ship %d of player %d destroyed' % (data['data'], data['id'])
                elif data['has_token'] == True:
                    struct_server['has_token'] = True
                else:
                    sock.sendto(pickle.dumps(dataReceiver), (struct_server['address']))
                    print 'Message[' + address[0] + ':' + str(address[1]) + ']:'
                    print data

        printTable()

    print "Todos os navios foram destruidos"
    sock.close()
