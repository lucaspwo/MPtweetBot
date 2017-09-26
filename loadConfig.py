def config():
    import socket, json

    val1 = ''
    val2 = ''
    val3 = ''
    val4 = ''

    flag = False

    preJson = open('config.txt').read()         # abertura do arquivo de configuracoes
    data = json.loads(preJson)
    config = data['campos']

    html = open('webConfig.html').read()        # abertura do arquivo com a pagina de configuracao

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # habilitando o socket
    s.bind(('', 80))
    s.listen(1)

    while flag == False:                        # percorrer enquanto a flag for falsa
        conn, addr = s.accept()
        request = conn.recv(1024)               # conteudo retornado pela pagina
        # print('content = %s' % str(request))
        request = str(request)
        ssid = request.find('ssid=')            # procurando pela string no retorno em string
        senha = request.find('senha=')          # retorna um inteiro, representando a posicao do
        freq = request.find('freq=')                #primeiro caractere da string procurada
        porc = request.find('porc=')
        # print(ssid)
        # print(usuar)
        if(ssid > 0 and ssid < 50):             # se a posicao for entre 0 e 50 (-1 e nao encontrado)
            str1 = ''
            cont = 0
            beg = ssid+5                        # o primeiro caractere a ser salvo vem apos a quantidade
            for i in request:                   #de caracteres da string procurada ("ssid=" = 5 caracteres)
                if cont >= beg:
                    if i != '&':                # enquanto o caractere nao for igual a "&" (separador de
                        str1 = str1 + i         #termos das respostas do formulario)
                    if i == '&':                # se for igual a "&", saia do laco for
                        break
                cont = cont + 1
            val1 = str1
        if(senha > 0 and senha < 50):           # busca da senha do wifi
            str2 = ''
            cont = 0
            beg = senha+6
            for i in request:
                if cont >= beg:
                    if i != '&':
                        str2 = str2 + i
                    if i == '&':
                        break
                cont = cont + 1
            val2 = str2
        if(freq > 0 and freq < 50):                 # busca do ip
            str3 = ''
            cont = 0
            beg = freq+5
            for i in request:
                if cont >= beg:
                    if i != '&':
                        str3 = str3 + i
                    if i == '&':
                        break
                cont = cont + 1
            val3 = str3
        if(porc > 0 and porc < 50):           # busca da senha do wifi
            str4 = ''
            cont = 0
            beg = porc+5
            for i in request:
                if cont >= beg:
                    if i != '\\' and i != ' ':
                        str4 = str4 + i
                    if i == '\\' or i == ' ':
                        break
                cont = cont + 1
            val4 = str4
        if val1 != '':                          # a impressao dos valores obtidos no formulario
            print('val1: ' + val1)              #junto com o armazenamento no vetor
            config[0] = val1
            flag = True
        if val2 != '':
            print('val2: ' + val2)
            config[1] = val2
            flag = True
        if val3 != '':
            print('val3: ' + val3)
            config[2] = val3
            flag = True                         # com a ultima variavel tendo sido modificada, mudar o valor da flag de controle
        if val4 != '':
            print('val4: ' + val4)
            config[3] = val4
            flag = True
        data['campos'] = config                 # escrita do vetor na biblioteca
        dataIn = json.dumps(data)               # passando a biblioteca para json
        f = open('config.txt', 'w')             # abrindo o arquivo de configuracoes
        f.write(dataIn)                         # escrevendo o json
        f.close()                               # fechando o arquivo
        response = html                         # enviando de volta a pagina de configuracoes
        conn.send(response)                     # NOTA: alterar para uma pagina de sucesso
        conn.close()                            # fechando a conexao
    s.close()                                   # fechando o socket de comunicacao
