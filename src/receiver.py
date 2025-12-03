import socket
import random

# Receptor configurações
TAMANHO_JANELA = 4       # Quantidade de frames na janela
HOST = "192.168.56.21"   # IP do receptor (pode ser 0.0.0.0 para escutar todas interfaces)
PORTA = 5000             # Porta UDP utilizada
LIMITE_FRAMES = 10       # Quantidade total de frames a enviar

# Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria socket UDP
sock.bind((HOST, PORTA))                                # Vincula o socket ao endereço e porta  
print("Receptor iniciado em {}:{}\n".format(HOST, PORTA))

# Variáveis de controle
frame_esperado = 1         # Próximo frame esperado
frames_recebidos = {}      # estrutura para armazenar frames recebidos fora de ordem

while frame_esperado <= LIMITE_FRAMES:
    # Receber dados do sender
    data, addr = sock.recvfrom(1024)  # Recebe até 1024 bytes
    msg = data.decode()
    
    if "FRAME" in msg:
        num = int(msg.split(":")[1])  # Extrai o número do frame recebido
        print("Recebido frame {}".format(num))

        # Simular perda de ACK/NACK (opcional, para teste de retransmissão)
        if random.random() < 0.1:
            print("[!] ACK/NACK perdido para frame {}".format(num))
            continue  # Não envia resposta, simula perda

        # Frame dentro da janela
        if frame_esperado <= num < frame_esperado + TAMANHO_JANELA:
            frames_recebidos[num] = True  # Marca o frame como recebido
            print("Frame {} armazenado".format(num))

            # Enviar ACK para todos os frames recebidos em ordem
            while frame_esperado in frames_recebidos:
                ack_msg = "ACK:{}".format(frame_esperado)
                sock.sendto(ack_msg.encode(), addr)
                print("Enviado {}".format(ack_msg))
                frame_esperado += 1

        # Frame fora da janela (antigo ou repetido)
        elif num < frame_esperado:
            # Reenvia ACK do frame já confirmado
            ack_msg = "ACK:{}".format(num)
            sock.sendto(ack_msg.encode(), addr)
            print("Reenviado {}".format(ack_msg))

        # Frame acima da janela (não esperado ainda)
        else:
            # Pode enviar NACK para informar que o frame anterior está faltando
            nack_msg = "NACK:{}".format(frame_esperado)
            sock.sendto(nack_msg.encode(), addr)
            print("Enviado {}".format(nack_msg))

print("Recepção completa!")