import machine, dht, time, tweet, neopixel
# pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

np = neopixel.NeoPixel(machine.Pin(4),1)
np[0] = (63,31,0)     # laranja
np.write()
TIME = time.time()
FLAG = False

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Teste</title> </head>
    <body> <h1>ESP8266 DHT11</h1>
        <table border="1"> <tr><th>Umidade (%):</th><th>Temperatura (C):</th></tr> %s </table>
    </body>
</html>
"""

d = dht.DHT11(machine.Pin(5))

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.setblocking(False)
s.listen(1)

print('listening on', addr)
np[0] = (0,31,0)     # verde
np.write()

while True:
    try:
        cl, addr = s.accept()
        FLAG = True
    except:
        if time.time() - TIME >= 30:    # trinta segundos
            np[0] = (0,31,0)     # verde
            np.write()
            d.measure()
            print ('Temp: %dºC' % d.temperature())
            print ('Umid: %d%%' % d.humidity())
            if d.humidity() >= 50:
                tweet.run(d.temperature(),d.humidity())
                tweet.send()
            TIME = time.time()
    if FLAG == True:
        np[0] = (0,0,63)     # azul
        np.write()
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