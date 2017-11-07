#coding: utf-8

# Name: Victor Picussa
# GRR: 20163068

# Imports
import math
import socket
import sys
import pickle
import time

# Servers info
PORT = 5050
servers = {}
servers['macalan'] = '200.17.202.6'
servers['orval'] = '200.17.202.28'
servers['h12'] = '10.254.223.16'
servers['h11'] = '10.254.223.15'
servers['h10'] = '10.254.223.14'
servers['h9'] = '10.254.223.13'
reverse = {}
reverse['200.17.202.6'] = 'macalan'
reverse['200.17.202.28'] = 'orval'
reverse['10.254.223.16'] = 'h12'
reverse['10.254.223.15'] = 'h11'
reverse['10.254.223.14'] = 'h10'
reverse['10.254.223.13'] = 'h9'
players = ['h12', 'h11']

# Initiatle the table
def init(N, S):
    global tableN, tableSize, table, numberShips
    tableN = N
    tableSize = N * N
    table = range(0, tableSize)
    for i in range(0, tableSize):
        table[i] = 0
    maxShips = math.floor(tableSize/6)
    numberShips = maxShips if S > maxShips else S

# Add a ship to the table
def addShip(line, column, type, s):
    type = type.upper()
    if type == 'L':
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
    elif type == 'C':
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

# Attack the player with the fiven coordenations
def attackCoord(line, column):
    global numberShips, tableN, table
    line -= 1
    column -= 1
    response = ""
    if line > (tableN-1) or line < 0 or column > (tableN-1) or column < 0:
        response = "Coordenadas fora do tabuleiro"
    else:
        if line == 0:
            if column == 0:
                if table[line*tableN + column] != 0:
                    auxiliar = table[line*tableN + column]
                    if (table[line*tableN + column+1] != auxiliar and
                    table[line*tableN + column+2] != auxiliar and
                    table[(line+1)*tableN + column] != auxiliar and
                    table[(line+2)*tableN + column] != auxiliar):
                        response =  "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
                else:
                    response = "Missil atingiu a agua"
            elif column == tableN-1:
                if table[line*tableN + column] != 0:
                    auxiliar = table[line*tableN + column]
                    if (table[line*tableN + column-1] != auxiliar and
                    table[line*tableN + column-2] != auxiliar and
                    table[(line+1)*tableN + column] != auxiliar and
                    table[(line+2)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
                else:
                    response = "Missil atingiu a agua"
            else:
                if table[line*tableN + column] != 0:
                    auxiliar = table[line*tableN + column]
                    if column < tableN-2 and column > 1:
                        if (table[line*tableN + column+1] != auxiliar and
                        table[line*tableN + column+2] != auxiliar and
                        table[line*tableN + column-1] != auxiliar and
                        table[line*tableN + column-2] != auxiliar and
                        table[(line+1)*tableN + column] != auxiliar and
                        table[(line+2)*tableN + column] != auxiliar):
                            response = "Navio %d destruido" % auxiliar
                            table[line*tableN + column] = 0
                            numberShips -= 1
                        else:
                            response = "Navio %d atingido" % auxiliar
                            table[line*tableN + column] = 0
                    elif column == tableN-2:
                        if (table[line*tableN + column+1] != auxiliar and
                        table[line*tableN + column-1] != auxiliar and
                        table[line*tableN + column-2] != auxiliar and
                        table[(line+1)*tableN + column] != auxiliar and
                        table[(line+2)*tableN + column] != auxiliar):
                            response = "Navio %d destruido" % auxiliar
                            table[line*tableN + column] = 0
                            numberShips -= 1
                        else:
                            response = "Navio %d atingido" % auxiliar
                            table[line*tableN + column] = 0
                    else:
                        if (table[line*tableN + column+1] != auxiliar and
                        table[line*tableN + column+2] != auxiliar and
                        table[line*tableN + column-1] != auxiliar and
                        table[(line+1)*tableN + column] != auxiliar and
                        table[(line+2)*tableN + column] != auxiliar):
                            response = "Navio %d destruido" % auxiliar
                            table[line*tableN + column] = 0
                            numberShips -= 1
                        else:
                            response = "Navio %d atingido" % auxiliar
                            table[line*tableN + column] = 0
                else:
                    response = "Missil atingiu a agua"
        elif line == tableN-1:
            if column == 0:
                if table[line*tableN + column] != 0:
                    auxiliar = table[line*tableN + column]
                    if (table[line*tableN + column+1] != auxiliar and
                    table[line*tableN + column+2] != auxiliar and
                    table[(line-1)*tableN + column] != auxiliar and
                    table[(line-2)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
                else:
                    response = "Missil atingiu a agua"
            elif column == tableN-1:
                if table[line*tableN + column] != 0:
                    auxiliar = table[line*tableN + column]
                    if (table[line*tableN + column-1] != auxiliar and
                    table[line*tableN + column-2] != auxiliar and
                    table[(line-1)*tableN + column] != auxiliar and
                    table[(line-2)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
                else:
                    response = "Missil atingiu a agua"
            else:
                if table[line*tableN + column] != 0:
                    auxiliar = table[line*tableN + column]
                    if column < tableN-2 and column > 1:
                        if (table[line*tableN + column+1] != auxiliar and
                        table[line*tableN + column+2] != auxiliar and
                        table[line*tableN + column-1] != auxiliar and
                        table[line*tableN + column-2] != auxiliar and
                        table[(line-1)*tableN + column] != auxiliar and
                        table[(line-2)*tableN + column] != auxiliar):
                            response = "Navio %d destruido" % auxiliar
                            table[line*tableN + column] = 0
                            numberShips -= 1
                        else:
                            response = "Navio %d atingido" % auxiliar
                            table[line*tableN + column] = 0
                    elif column == tableN-2:
                        if (table[line*tableN + column+1] != auxiliar and
                        table[line*tableN + column-1] != auxiliar and
                        table[line*tableN + column-2] != auxiliar and
                        table[(line-1)*tableN + column] != auxiliar and
                        table[(line-2)*tableN + column] != auxiliar):
                            response = "Navio %d destruido" % auxiliar
                            table[line*tableN + column] = 0
                            numberShips -= 1
                        else:
                            response = "Navio %d atingido" % auxiliar
                            table[line*tableN + column] = 0
                    else:
                        if (table[line*tableN + column+1] != auxiliar and
                        table[line*tableN + column+2] != auxiliar and
                        table[line*tableN + column-1] != auxiliar and
                        table[(line-1)*tableN + column] != auxiliar and
                        table[(line-2)*tableN + column] != auxiliar):
                            response = "Navio %d destruido" % auxiliar
                            table[line*tableN + column] = 0
                            numberShips -= 1
                        else:
                            response = "Navio %d atingido" % auxiliar
                            table[line*tableN + column] = 0
                else:
                    response = "Missil atingiu a agua"
        elif column == 0:
            if table[line*tableN + column] != 0:
                auxiliar = table[line*tableN + column]
                if line < tableN-2 and line > 1:
                    if (table[line*tableN + column+1] != auxiliar and
                    table[line*tableN + column+2] != auxiliar and
                    table[(line+1)*tableN + column] != auxiliar and
                    table[(line+2)*tableN + column] != auxiliar and
                    table[(line-1)*tableN + column] != auxiliar and
                    table[(line-2)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
                elif line == tableN-2:
                    if (table[line*tableN + column+1] != auxiliar and
                    table[line*tableN + column+2] != auxiliar and
                    table[(line+1)*tableN + column] != auxiliar and
                    table[(line-1)*tableN + column] != auxiliar and
                    table[(line-2)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
                else:
                    if (table[line*tableN + column+1] != auxiliar and
                    table[line*tableN + column+2] != auxiliar and
                    table[(line+1)*tableN + column] != auxiliar and
                    table[(line+2)*tableN + column] != auxiliar and
                    table[(line-1)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
            else:
                response = "Missil atingiu a agua"
        elif column == tableN-1:
            if table[line*tableN + column] != 0:
                auxiliar = table[line*tableN + column]
                if line < tableN-2 and line > 1:
                    if (table[line*tableN + column-1] != auxiliar and
                    table[line*tableN + column-2] != auxiliar and
                    table[(line+1)*tableN + column] != auxiliar and
                    table[(line+2)*tableN + column] != auxiliar and
                    table[(line-1)*tableN + column] != auxiliar and
                    table[(line-2)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
                elif line == tableN-2:
                    if (table[line*tableN + column-1] != auxiliar and
                    table[line*tableN + column-2] != auxiliar and
                    table[(line+1)*tableN + column] != auxiliar and
                    table[(line-1)*tableN + column] != auxiliar and
                    table[(line-2)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
                else:
                    if (table[line*tableN + column-1] != auxiliar and
                    table[line*tableN + column-2] != auxiliar and
                    table[(line+1)*tableN + column] != auxiliar and
                    table[(line+2)*tableN + column] != auxiliar and
                    table[(line-1)*tableN + column] != auxiliar):
                        response = "Navio %d destruido" % auxiliar
                        table[line*tableN + column] = 0
                        numberShips -= 1
                    else:
                        response = "Navio %d atingido" % auxiliar
                        table[line*tableN + column] = 0
            else:
                response = "Missil atingiu a agua"
        else:
            if table[line*tableN + column] != 0:
                auxiliar = table[line*tableN + column]
                if (table[line*tableN + column+1] != auxiliar and
                table[line*tableN + column+2] != auxiliar and
                table[line*tableN + column-1] != auxiliar and
                table[line*tableN + column-2] != auxiliar and
                table[(line-1)*tableN + column] != auxiliar and
                table[(line-2)*tableN + column] != auxiliar and
                table[(line+1)*tableN + column] != auxiliar and
                table[(line+2)*tableN + column] != auxiliar):
                    response = "Navio %d destruido" % auxiliar
                    table[line*tableN + column] = 0
                    numberShips -= 1
                else:
                    response = "Navio %d atingido" % auxiliar
                    table[line*tableN + column] = 0
            else:
                response = "Missil atingiu a agua"
    return response

# Print the table
def printTable():
    global tableN, table

    print '\n\t' + ('-- ' * tableN)
    for i in range(0, tableN):
        print '\t| ' + ' '.join(str(x) for x in table[i*tableN:i*tableN+tableN]) + ' |'
    print '\t' + ('-- ' * tableN) + '\n'

# Create socket server and make connection to the target server
def connection(ID, HOST, TARGET):
    global sock, struct_server

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print '\nCONEXÃO: Criação do socket feita com sucesso!'
    except:
        print 'CONEXÃO: Criação do socket falhou! Saindo...'
        sys.exit()

    struct_server = {
        'id'       : ID,
        'host'     : (HOST, PORT),
        'port'     : PORT,
        'has_token': False,
        'target'   : (TARGET, PORT),
        'winner'   : 0
    }

    struct_server.update({'address': (struct_server['host'], struct_server['port'])})

    while True:
        try:
            sock.bind(struct_server['host'])
            print '\nCONEXÃO: Socket vinculado com sucesso em %s' % struct_server['target'][0]
            break
        except socket.error:
            print '\nErro ao conectar socket! Tentando novamente...'
            time.sleep(5)
            continue

# Initiate the game
def play():
    ID = sys.argv[1]
    HOST = servers[sys.argv[1]]
    TARGET = servers[sys.argv[2]]
    # Make the connection
    connection(ID, HOST, TARGET)

    if '--token' in sys.argv:
        struct_server['has_token'] = True

    times = int((50-(22+len(sys.argv[1])))/2)
    print "##################################################"
    print "#"*times + "  Bem vindo jogador" + sys.argv[1] + "!  " + "#"*times

    # Read inputs for the table
    while True:
        try:
            n = int(raw_input("\n> Tamanho do tabulerio : "))
            s = int(raw_input("\n> Quantidade de navios : "))
            break
        except ValueError:
            print "\n ERRO: As entradas devem ser números inteiros!"
            continue


    # Initialize the table
    init(n, s)

    # Add the ships to a given coordenation
    while s:
        coordenations = raw_input("\n> Coordenadas e tipo(linha,coluna,tipo): ")
        coordenations = coordenations.split(',')
        if len(coordenations) != 3:
            print "\nERRO: Devem haver necessariamente 2 coordenadas e 1 tipo!"
            continue
        if coordenations[2].upper() != "L" and coordenations[2].upper() != "C":
            print "\nERRO: Os tipos de coordenada devem ser C ou L!"
            continue
        try:
            int(coordenations[0])
            int(coordenations[1])
        except ValueError:
            print "\nERRO: As coordenadas devem ser números inteiros!"
            continue
        validate = addShip(int(coordenations[0]), int(coordenations[1]), coordenations[2], s)
        if validate:
            s -= 1

    # Show the table
    printTable()

    # While has ships and the there's no winner
    while struct_server['id'] in players and len(players)-1:
        if struct_server['has_token']:
            # If the player has the token, then he can strike someone
            print "\nÉ a sua vez!"

            # Create the message to be sent
            data = {
                'id'       : struct_server['id'],
                'host'     : struct_server['host'],
                'port'     : struct_server['port'],
                'origin'   : struct_server['address'],
                'destiny'  : '',
                'type'     : 'A',
                'has_token': False,
                'data'     : '',
                'received' : 0,
                'winner'   : ''
            }

            # Choose a player to attack
            player = raw_input("\n> Escolha um jogador: ")
            while (player == struct_server['id']) or (player not in players):
                print '\nERRO: Impossível atacar jogador %s!' % player
                player = raw_input("\n> Escolha um jogador: ")

            data['destiny'] = player

            # Choose where to strike
            while True:
                coordenations = raw_input("\n> Coordenadas de ataque (linha,coluna): ")
                coordenations = coordenations.split(',')
                if len(coordenations) != 2:
                    print "\nERRO: Devem haver necessariamente 2 coordenadas!"
                    continue
                try:
                    int(coordenations[0])
                    int(coordenations[1])
                except ValueError:
                    print "\nERRO: As coordenadas devem ser números inteiros!"
                    continue
                break

            data['data'] = coordenations

            while not data['received']:
                try:
                    sock.settimeout(20)
                    sock.sendto(pickle.dumps(data), (struct_server['target']))
                except socket.error, message:
                    print '\nCONEXÃO: Erro ao mandar mensagem! Tentando novamente...'
                    sock.settimeout(None)
                    time.sleep(2)
                    continue
                try:
                    dataReceiver = sock.recvfrom(4096)
                except socket.timeout:
                    print '\nCONEXÃO: Mensagem perdida! Tentando novamente...'
                    sock.settimeout(None)
                    time.sleep(2)
                    continue
                sock.settimeout(None)
                data = pickle.loads(dataReceiver[0])
                address = dataReceiver[1]

                if data['received']:
                    if data['type'] == 'DX':
                        data['data'] = data['data'] + ' do jogador ' + data['destiny'] + '!'
                        print '\n' + data['data']
                        data['type'] = 'D'
                        data['received'] = 0
                    # If the message has type E, print player data and remove from players
                    elif data['type'] == 'EX':
                        print '\n' + data['data']
                        players.remove(data['destiny'])
                        data['type'] = 'E'
                        data['received'] = 0
                    elif data['type'] != 'D' and data['type'] != 'E':
                        print '\n' + data['data']

            # Create the message to send token
            data = {
                'id'       : struct_server['id'],
                'host'     : struct_server['host'],
                'port'     : struct_server['port'],
                'origin'   : struct_server['address'],
                'destiny'  : struct_server['target'],
                'type'     : 'T',
                'has_token': True,
                'received' : 0,
                'winner'   : ''
            }

            # Send token message
            while True:
                try:
                    sock.sendto(pickle.dumps(data), (struct_server['target']))
                    struct_server['has_token'] = False
                    break
                except socket.error, message:
                    print '\nCONEXÃO: Erro ao mandar mensagem! Tentando novamente...'
                    time.sleep(2)
                    continue
        else:
            # If the player doesn't have the token, he wait for it
            print '\nAguardando jogadores...'
            while not struct_server['has_token'] and struct_server['id'] in players:
                dataReceiver = sock.recvfrom(4096)
                data = pickle.loads(dataReceiver[0])
                address = dataReceiver[1]

                if data['type'] == 'T' and data['has_token'] == True:
                    struct_server['has_token'] = True
                else:
                    # If the message has type D, print ship destroyed
                    if data['type'] == 'D' and data['destiny'] != struct_server['id']:
                        print '\n' + data['data']
                        data['received'] = 1
                    # If the message has type E, print player data and remove from players
                    elif data['type'] == 'E':
                        print '\n' + data['data']
                        data['received'] = 1
                        players.remove(data['destiny'])
                    # If the message destiny is equal to server id, then intercept it
                    elif data['destiny'] == struct_server['id']:
                        data['received'] = 1
                        if data['type'] == 'A':
                            print '\nAtaque recebido do jogador %s nas coordenadas (%s, %s)!' % (data['id'], data['data'][0], data['data'][1])
                            data['data'] = attackCoord(int(data['data'][0]), int(data['data'][1]))
                            print '\n' + data['data']
                            if not numberShips:
                                print "\nTodos os seus navios foram destruidos!"
                                data['type'] = 'EX'
                                data['data'] = 'Jogador %s eliminado!' % struct_server['id']
                            elif 'destruido' in data['data']:
                                data['type'] = 'DX'
                            printTable()
                    # If the message has type T, then get the token
                    while True:
                        try:
                            sock.sendto(pickle.dumps(data), (struct_server['target']))
                            break
                        except socket.error, message:
                            print '\nCONEXÃO: Erro ao mandar mensagem! Tentando novamente...'
                            continue

    # If player has no ship, then he didn't won the game and need to wait the end
    if not numberShips:
        print "\nEsperando o jogo terminar..."

        # Wait for the winner
        while not struct_server['winner']:
            dataReceiver = sock.recvfrom(4096)
            data = pickle.loads(dataReceiver[0])
            address = dataReceiver[1]

            if data['type'] == 'W':
                struct_server['winner'] = data['winner']
                print '\n' + data['data']
                data['received'] = 1
                while True:
                    try:
                        sock.sendto(pickle.dumps(data), (struct_server['target']))
                        break
                    except socket.error, message:
                        print '\nErro ao mandar mensagem! Tentando novamente...'
                        time.sleep(2)
                        continue
            else:
                while True:
                    try:
                        sock.sendto(dataReceiver[0], (struct_server['target']))
                        break
                    except socket.error, message:
                        print '\nErro ao mandar mensagem! Tentando novamente...'
                        time.sleep(2)
                        continue
    else:
        print "\nVocê é o vencedor!"

        # Create the message to send token
        data = {
            'id'       : struct_server['id'],
            'host'     : struct_server['host'],
            'port'     : struct_server['port'],
            'origin'   : struct_server['address'],
            'destiny'  : struct_server['target'],
            'type'     : 'W',
            'has_token': False,
            'received' : 0,
            'winner'   : struct_server['id']
        }

        data['data'] = 'O jogador vencedor é ' + data['id'] + '!'

        while not data['received']:
            try:
                sock.settimeout(20)
                sock.sendto(pickle.dumps(data), (struct_server['target']))
                break
            except socket.error, message:
                print '\nErro ao mandar mensagem! Tentando novamente...'
                sock.settimeout(None)
                time.sleep(2)
                continue
    	    try:
                dataReceiver = sock.recvfrom(4096)
            except socket.timeout:
                print '\nCONEXÃO: Mensagem perdida! Tentando novamente...'
                sock.settimeout(None)
                time.sleep(2)
                continue
            sock.settimeout(None)
    	    data = pickle.loads(dataReceived[0])
    	    address = dataReceived[1]

    # Close the game
    print '\nFechando o jogo...'
    time.sleep(3)
    sock.close()

play()
