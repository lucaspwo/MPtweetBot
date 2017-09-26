def run():
    import machine, dht, time, json, neo
    # pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

    btn = machine.Pin(14, machine.Pin.IN)
    # np = neopixel.NeoPixel(machine.Pin(4),1)
    # np[0] = (63,31,0)     # laranja
    # np.write()
    TIME = time.time()
    FLAG = False
    FLAG2 = False
    global RESET
    RESET = False

    preJson = open('config.txt').read()         # abertura do arquivo de configuracoes
    data = json.loads(preJson)
    config = data['campos']

    html = open('index.html').read()

#     html = """<!DOCTYPE html>
# <html>
#     <head> <title>ESP8266 Teste</title> </head>
#     <body> <h1>ESP8266 DHT11</h1>
#         <table border="1"> <tr><th>Umidade (%):</th><th>Temperatura (C):</th></tr> %s </table>
#     </body>
# </html>
# """

    d = dht.DHT11(machine.Pin(5))

    import socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.setblocking(False)
    s.listen(1)

    def cb(change):
        global RESET
        RESET = True

    btn.irq(trigger= machine.Pin.IRQ_FALLING, handler=cb)

    print('listening on', addr)
    neo.run(0,31,0)
    # np[0] = (0,31,0)     # verde
    # np.write()

    try:
        while True:
            try:
                cl, addr = s.accept()
                FLAG = True
            except:
                if FLAG2 == True:
                    machine.reset()
                if RESET == True:
                    config2 = ['wifi', 'senha', '10', '10']
                    data['campos'] = config2                 # escrita do vetor na biblioteca
                    dataIn = json.dumps(data)               # passando a biblioteca para json
                    f = open('config.txt', 'w')             # abrindo o arquivo de configuracoes
                    time.sleep(1)
                    f.write(dataIn)                         # escrevendo o json
                    time.sleep(1)
                    f.close()                               # fechando o arquivo
                    time.sleep(2)
                    RESET = False
                    FLAG2 = True
                    # machine.reset()

                if time.time() - TIME >= int(config[2]):    # trinta segundos
                    neo.run(0,31,0)
                    # np[0] = (0,31,0)     # verde
                    # np.write()
                    d.measure()
                    print ('Temp: %dºC' % d.temperature())
                    print ('Umid: %d%%' % d.humidity())
                    if d.humidity() >= int(config[3]):
                        neo.run(63,0,0)
                        import tweet
                        tweet.run(d.temperature(),d.humidity())
                        # tweet.send()
                    TIME = time.time()
            if FLAG == True:
                neo.run(0,0,63)
                # np[0] = (0,0,63)     # azul
                # np.write()
                TIME = time.time()
                FLAG = False
                print('client connected from', addr)
                cl_file = cl.makefile('rwb', 0)
                while True:
                    d.measure()
                    line = cl_file.readline()
                    if not line or line == b'\r\n':
                        break
                rows = ['<tr><td>%d</td><td>%d</td></tr>' % (d.humidity(), d.temperature())]
                response = html % '\n'.join(rows)
                cl.send(response)
                cl.close()
    finally:
        s.close()
        neo.run(0,0,0)