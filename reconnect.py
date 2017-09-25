import network, utime, ubinascii, json, loadConfig

wlan = network.WLAN(network.STA_IF)     # criacao do objeto wlan
wlan.active(True)                       # certificando que o wifi esta ativo

preJson = open('config.txt').read()     # leitura do arquivo de configuracao
data = json.loads(preJson)              # interpretacao do json e associacao a uma biblioteca
config = data['campos']                 # armazenamento dos campos em um vetor

count = 0                               # contador para ativar o modo de configuracao

def connect():
    wlan.connect(config[0], config[1])      # instrucao de conexao ao wifi armazenado (ssid, senha)

    while not wlan.isconnected():           # enquanto nao estiver conectado
        utime.sleep(1)                      # espere 1 segundo
        global count
        count = count +1                    # incremente o contador em 1
        if(count == 10):                    # se passarem 10 segundos sem conexao, iniciar a reconfiguracao
            init()

def init():
    wlan.active(False)              # desativacao do wlan infraestrutura
    ssid=str(ubinascii.hexlify(wlan.config('mac')))[8:-1]   # recuperacao o endereco mac, converter para hexadecimal, converter para string e manter apenas os ultimos caracteres
    ap = network.WLAN(network.AP_IF)# criacao do objeto ap
    ap.active(True)                 # ativacao da rede ap
    ap.config(essid='ESP_Config-'+ssid, authmode=network.AUTH_WPA_WPA2_PSK, password='bonooliveira'+ssid)     # reconfiguracao das informacoes da rede: criacao de ssid e senha unicos, por esp
    loadConfig.config()             # abertura do programa para reconfiguracao
    wlan.active(True)               # apos alteracao das configuracoes, reativar a rede wlan
    ap.active(False)                # desativacao da rede ap
    preJson2 = open('config.txt').read()    # recarregamento do txt de configuracoes
    data2 = json.loads(preJson2)            # armazenamento na biblioteca
    config2 = data2['campos']               # armazenamento em vetor
    wlan.connect(config2[0], config2[1])    # instrucao de conexao na nova rede wifi
    global count
    count = 0                       # reiniciar o contador, dando mais 10 segundos para conectar, antes de reiniciar o processo
