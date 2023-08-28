#################################################################
# -*- coding: latin-1 -*-
# pecrc.py - protocolo ponto-a-ponto simples com retransmissão
#          - entrega interface semelhante a um socket
#################################################################
# fornece a classe PECRC, que tem os métodos:
#
# contrutor: pode receber um ou dois parâmetros, para criar um
#            canal que implementa o protocolo PECRC;
#            - o servidor cria o objeto apenas com o porto;
#            - o cliente cria o objeto com host e porto.
# close: encerra o enlace
# send(m): envia o array de bytes m pelo canal, calculando o 
#           checksum, fazendo o enquadramento e controlando a
#           retransmissão, se necessário.
# recv(): recebe um quadro e retorna-o como um array de bytes,
#         conferindo o enquadramento, conferindo o checksum e
#         enviando uma mensagem de confirmação, se for o caso.
# OBS: o tamanho da mensagem enviada/recebida pode variar, 
#      mas não deve ser maior que 1500 bytes.
################################################################
# PECRC utiliza o módulo canal_tp1 como API para envio e recepção
#        pelo enlace; o qual não deve ser alterado.
# PECRC não pode utilizar a interface de sockets diretamente.
################################################################

import canal_tp1

class PECRC:
  
    separador_mensagem = '$%#$%#'
    Bytes_Bytestuffing = '[]'
    def __init__(self, port, host='' ):
        self.link = canal_tp1.Link(port,host)

    def close(self):
        self.link.close()
        
####################################################################
# A princípio, só é preciso alterar as duas funções a seguir.
  
    # -------------------------------------------------------------------------------------------------
    def send(self,message):
            # Aqui, PPSRT deve fazer:
            #   - fazer o encapsulamento de cada mensagem em um quadro,
            #   - calcular o Checksum do quadro e incluído,
            checksum = self.Checksum(message)
            #   - fazer o byte stuffing durante o envio da mensagem,
            mensagemComBytestuffing = self.ColocarByteStuffing(str(message), self.Bytes_Bytestuffing)
            mensagem_envio = self.EncapsulamentoQuadro(mensagemComBytestuffing, 'D', '1', checksum)
            self.link.send(bytes(mensagem_envio, 'utf-8'))
            
            try:
                frame = self.link.recv(1500)
                print(frame)
            except TimeoutError: # use para tratar temporizações
                print("Timeout") # cuidaria da retransmissão


    # -------------------------------------------------------------------------------------------------
    def recv(self):
        # Aqui, PPSRT deve fazer:
        #   - identificar começo de um quadro,
        #   - receber a mensagem byte-a-byte, para retirar o stuffing,
        #   - detectar o fim do quadro,
        #   - calcular o checksum do quadro recebido,
        #   - descartar silenciosamente quadros com erro,
        #   - enviar uma confirmação para quadros recebidos corretamente,
        self.link.send(bytes('C', 'utf-8'))
        #   - conferir a ordem dos quadros e descartar quadros repetidos.
        return self.link.recv(1500)
    
    # -------------------------------------------------------------------------------------------------
    def Checksum(self, informacao):
        checksum = 0
        
        # Abaixo está a lógica do Checksum. Caso deseje alterá-la basta mudar a seção de código abaixo
        
        for i in range(len(informacao)):
            # checksum += i * ord(informacao[i])
            checksum = 211
        
        # print('A checksum da informação \n{\n' + informacao + '\n}\neh:' + str(checksum) )
        return checksum % pow(2,16)

    # -------------------------------------------------------------------------------------------------
    def VerificaChecksum(self, informacao, ValorChecksum):
        checksum = self.Checksum(informacao)
            
        if(ValorChecksum == checksum):
            # print('A informação chegou perfeitamente')
            return True
        else:
            # print('A informação não chegou perfeitamente')
            return False
        
    # -------------------------------------------------------------------------------------------------    
    def ColocarByteStuffing(self, mensagem, _bytes):
        for i in range(len(_bytes)):
            mensagem = mensagem.replace(_bytes[i], '!' + _bytes[i])
        return mensagem
    
    # -------------------------------------------------------------------------------------------------
    def RetirarByteStuffing(self, mensagem, _bytes):
        for i in range(len(_bytes)):
            mensagem = mensagem.replace('!' + _bytes[i], _bytes[i])
        return mensagem
    
    # -------------------------------------------------------------------------------------------------
    #Todas os parâmetros vão estar corretos e e como string
    def EncapsulamentoQuadro(self,mensagem,controle,pacote,cksum_quadro):
        quadro = '[' + controle + self.separador_mensagem + pacote + self.separador_mensagem + mensagem + self.separador_mensagem + str(cksum_quadro) + ']'
        return quadro