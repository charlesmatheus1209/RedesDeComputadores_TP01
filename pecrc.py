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
        if str(message) == "//MensagemDeConfirmacao//":
            # Aqui, PPSRT deve fazer:
            #   - fazer o encapsulamento de cada mensagem em um quadro,
            #   - calcular o Checksum do quadro e incluído,
            checksum = self.Checksum(message.decode('utf-8'))
            #   - fazer o byte stuffing durante o envio da mensagem,
            mensagemComBytestuffing = self.ColocarByteStuffing(message.decode('utf-8'), self.Bytes_Bytestuffing)
            mensagem_envio = self.EncapsulamentoQuadro(mensagemComBytestuffing, 'C', '1', checksum)
            self.link.send(bytes(mensagem_envio, 'utf-8'))
            return 'Vazio'
            
        else:
            # Lista para armazenar os blocos de 3 caracteres
            MensagemDecodificada = message.decode('utf-8')
            blocos = []

            # Itera pela string em incrementos de 1500 bytes
            for i in range(0, len(MensagemDecodificada), 1500):
                if(i + 1500 > len(MensagemDecodificada)):
                    bloco = MensagemDecodificada[i:len(MensagemDecodificada)-1]  # Pega os próximos 1500 bytes
                    blocos.append(bloco)
                else:
                    bloco = MensagemDecodificada[i:i+1500]  # Pega os próximos 1500 bytes
                    blocos.append(bloco)

            #print(blocos)    
            # Exibe os blocos de 1500 bytes
            print(len(blocos))
            for i in range(len(blocos)):
            
                checksum = self.Checksum(bloco)
                mensagemComBytestuffing = self.ColocarByteStuffing(bloco, self.Bytes_Bytestuffing)
                mensagem_envio = self.EncapsulamentoQuadro(mensagemComBytestuffing, 'D', str(i), checksum)
                self.link.send(bytes(mensagem_envio, 'utf-8'))
            
            try:
                frame = self.link.recv(1500)
            except TimeoutError: # use para tratar temporizações
                print("Timeout") # cuidaria da retransmissão
                checksum = self.Checksum(message)
                mensagemComBytestuffing = self.ColocarByteStuffing(message.decode('utf-8'), self.Bytes_Bytestuffing)
                mensagem_envio = self.EncapsulamentoQuadro(mensagemComBytestuffing, 'D', '1', checksum)
                self.link.send(bytes(mensagem_envio, 'utf-8'))
            
    


    # -------------------------------------------------------------------------------------------------
    def recv(self):
        # Aqui, PPSRT deve fazer:
        #   - identificar começo de um quadro,
        Bframe = self.link.recv(1500)
        frame = str(Bframe)
        # print(frame)
        if frame[2] == '[' and frame[-2] == ']':
            print('Frame Completo')
            
            lista = self.DesencapsulaQuadro(frame)
            informacao = self.RetirarByteStuffing(lista[2], self.Bytes_Bytestuffing)
            check = self.VerificaChecksum(informacao, lista[3])
            
            if check == True:
                self.send(bytes('//MensagemDeConfirmacao//', 'utf-8'))
                
            print(check)
            
        else:
            print('Frame incompleto')
        
        
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
        
        if(int(ValorChecksum) == checksum):
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

    def DesencapsulaQuadro(self, quadro):
        quadro_recuperado = quadro.replace(self.Bytes_Bytestuffing,"")
        return quadro_recuperado
    
    def DesencapsulaQuadro(self, quadro):
        sMarcador = quadro[3:-2]
        lista = sMarcador.split("$%#$%#")
        return lista