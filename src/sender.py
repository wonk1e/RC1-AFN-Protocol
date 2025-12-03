import socket    # Para comunicação via rede
import time      # Para controlar delays
import random    # Para simular perda de pacotes

# Protocolo
TAMANHO_JANELA = 4       # Quantidade de frames na janela
HOST = "192.168.56.21"   # Endereço IP do receptor
PORTA = 5000             # Porta UDP utilizada
LIMITE_FRAMES = 10       # Quantidade total de frames a enviar

# Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria socket UDP
sock.settimeout(2)                                       # Tempo de 2s para esperar ACK/NACK

# Variáveis de controle
base_janela = 1                 # Primeiro frame da janela
proximo_frame = 1               # Próximo frame a ser enviado
ack_recebidos = set()           # Conjunto de ACK recebidos

# Função para enviar um frame
def enviar_frame(num):
    """
    Envia o frame 'num' para o receptor.
    Simula perda de pacote com 20% de chance.
    """
    print("Enviando frame {}".format(num))

    # Simular perda de pacotes de forma aleatória
    if random.random() < 0.2:
        print("[x] Frame {} perdido".format(num))
        return

    # Enviar o frame via UDP
    sock.sendto("FRAME:{}".format(num).encode(), (HOST, PORTA))

while base_janela <= LIMITE_FRAMES:

    # Enviar frames até preencher a janela
    while proximo_frame < base_janela + TAMANHO_JANELA and proximo_frame <= LIMITE_FRAMES:
        enviar_frame(proximo_frame)
        proximo_frame += 1

    # Aguardar ACK/NACK do receptor
    try:
        data, _ = sock.recvfrom(1024)  # Recebe dados do receptor (até 1024 bytes)
        msg = data.decode()            # Decodifica a mensagem recebida

        # Se for ACK
        if "ACK" in msg:
            num = int(msg.split(":")[1])  # Extrai o número do frame confirmado
            print("Recebido ACK de {}".format(num))
            ack_recebidos.add(num)        # Adiciona ao conjunto de ACKs recebidos

            # Avança a base da janela enquanto o frame da base tiver sido confirmado
            while base_janela in ack_recebidos:
                base_janela += 1

        # Se for NACK
        elif "NACK" in msg:
            num = int(msg.split(":")[1])  # Extrai o número do frame que precisa ser reenviado
            print("Recebido NACK de {} -> reenviando".format(num))
            enviar_frame(num)             # Reenvia o frame indicado

    # Se ocorrer timeout (nenhum ACK/NACK recebido no tempo limite)
    except socket.timeout:
        print("Timeout -> reenviar frames não confirmados")
        # Reenvia todos os frames que ainda não foram confirmados
        for i in range(base_janela, proximo_frame):
            if i not in ack_recebidos:
                enviar_frame(i)

print("Transmissão completa!")
sock.close()  # Fecha o socket UDP