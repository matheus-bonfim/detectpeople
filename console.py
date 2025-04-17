import threading
import time

# Estado compartilhado
estado = {
    "ativo": True,
    "rodando": True
}

# Função que escuta comandos no console
def escutar_comandos():
    while estado["rodando"]:
        comando = input().strip().lower()
        if comando == "status":
            print(f"[Status] Programa está {'ativo' if estado['ativo'] else 'pausado'}")
        elif comando == "pause":
            estado["ativo"] = False
            print("[Comando] Execução pausada.")
        elif comando == "resume":
            estado["ativo"] = True
            print("[Comando] Execução retomada.")
        elif comando == "parar":
            estado["rodando"] = False
            print("[Comando] Encerrando o programa.")
        else:
            print(f"[Erro] Comando desconhecido: {comando}")

# Inicia a thread de escuta
thread_entrada = threading.Thread(target=escutar_comandos)
thread_entrada.daemon = True
thread_entrada.start()

# Programa principal
print("Programa iniciado. Comandos: status, pause, resume, parar")
contador = 0

while estado["rodando"]:
    if estado["ativo"]:
        print(f"Executando... {contador}")
        contador += 1
    else:
        print("...pausado...")
    time.sleep(1)

print("Programa finalizado.")
