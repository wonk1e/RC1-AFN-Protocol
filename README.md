===== Protocolo de Aplicação Selectiva (AFN/ Selective Repeat ARQ) ====

O AFN (Aplicação de Frames Negativos) ou Selective Repeat ARQ é um protocolo de controlo de erros que permite que o receptor peça apenas os frames (pacotes) que chegaram com erros ou não chegaram, em vez de repetir tudo o que veio depois.

É eficiente em ligações com:
	* atraso elevado
	* taxa de erro relactivamente constante
	* quando se pretende aumentar o throughput


# Modo de Funcionamento
O funcionamento está dividido em 6 partes. Cada parte corresponde a um passo lógico do protocolo.
Estas partes são:

1.	Janela de Transmissão (sliding window)
* define quais frames podem ser enviados ou aceites naquele momento;
* desliza conforme vão chegando ACKs

2.	Envio de Frames
* o emissor envia tudo o que está na janela sem esperar receber o ACK
* cada frame fica à espera dentro do buffer do emissor até ser confirmado

3.	Verificação no Receptor
* cada frame é analisado individualmente pelo receptor
se:
	chegar correcto: é guardado
	chegar corrompido: é descartado
	não chegar: nada acontece até o receptor perceber por timeout

4.	NACK ou Timeout (pedido de retransmissão)
Métodos de detenção:
	* NACK(<codigo_pacote>)
	* Timeout: o receptor perceber que o ACK(<codigo_pacote>) não chegou a tempo e decide reenviar

5.	Retransmissão Selectiva
O emissor só reenvia o frame em falta, nada mais.

6.	Reordenamento
O receptor reorganiza em função da ordem dos pacotes 
