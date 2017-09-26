import mpbot, reconnect, neo, gc, utime

neo.run(63,31,0)

while(True):
    reconnect.connect()
    gc.collect()
    mpbot.run()                    # havendo sucesso na conexao, executar o codigo principal
