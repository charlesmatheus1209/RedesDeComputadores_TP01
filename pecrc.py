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
  
    
    Bytes_Bytestuffing = '[]'
    
    def __init__(self, port, host='' ):
        self.link = canal_tp1.Link(port,host)

    def close(self):
        self.link.close()
        
####################################################################
# A princípio, só é preciso alterar as duas funções a seguir.
  
    # -------------------------------------------------------------------------------------------------
    def send(self,message):
        # print(message)
        MsgComByteStuffing = self.ColocarByteStuffing(message.decode(), self.Bytes_Bytestuffing)
        # print(MsgComByteStuffing)
        
        blocos = self.separaTamanho(MsgComByteStuffing, 9)
        NumeroDoQuadro = '0'
        j = 0
        for i in range(0, len(blocos)):  
            bloco = blocos[i - j]   
            Checksum = self.Checksum(bloco)
            print("Checksum: " + Checksum)
            quadro = list()

            quadro.append(bytes('[', 'utf-8'))
            quadro.append(bytes('D', 'utf-8'))
            quadro.append(bytes(NumeroDoQuadro, 'utf-8'))
            quadro.append(bytes(bloco, 'utf-8'))
            quadro.append(bytes(str(Checksum),'utf-8'))
            quadro.append(bytes(']', 'utf-8'))
            
            quadroEnviar = b''.join(quadro)
            
            print("QuadroEnviar: ", quadroEnviar)
            
            self.link.send(quadroEnviar)
            
            try:
                frame = self.link.recv(1500)
                print(frame)
                
                if(not frame): raise TimeoutError
                    
                print('Chegou')
                
                if NumeroDoQuadro == '0':
                    NumeroDoQuadro = '1'
                else:
                    NumeroDoQuadro = '0'
            except TimeoutError: # use para tratar temporizações
                print("Timeout") # cuidaria da retransmissão 
                j += 1 



    def recv(self):
        
        print("------------Inicio Pecrc.Recv-----------")
            
        NquadroAnterior = bytes('1', 'utf-8')
        while True:
            MENSAAGEMFINAL = bytes()
            resp = bytes('', 'utf-8')
            recebidoCompleto = False
            byteRecebido = self.link.recv(1)
            # Inicio de Quadro
            if(byteRecebido == bytes('[', 'utf-8')):
                DouC = self.link.recv(1)
                Controle = self.link.recv(1)
                            
                while True:
                    byteRecebido = self.link.recv(1)
                    if(byteRecebido == bytes('!', 'utf-8')):
                        byteRecebido = self.link.recv(1)
                        MENSAAGEMFINAL += byteRecebido
                        continue
                    # print(byteRecebido)
                    MENSAAGEMFINAL += byteRecebido
                    if(byteRecebido == bytes(']', 'utf-8')):
                        recebidoCompleto = True
                        break
                    
                if(recebidoCompleto == True):
                    checkRecebido = MENSAAGEMFINAL[(len(MENSAAGEMFINAL)-3):(len(MENSAAGEMFINAL)-1)]
                    MensagemRecebida = MENSAAGEMFINAL[0:(len(MENSAAGEMFINAL)-3)]
                    print("Mensagem recebida: ", (MensagemRecebida))
                    print("Controle: ", Controle)
                    print("Controle Anterir: ", NquadroAnterior)
                    if((self.Checksum(MensagemRecebida.decode()) == checkRecebido.decode()) and (Controle != NquadroAnterior) ):
                        resp = MensagemRecebida
                        
                        NquadroAnterior = Controle
                        print("Entrei")
                        self.link.send(bytes('[C{}]'.format(Controle.decode()), 'utf-8'))
                    else:
                        print("Nao Entrei")
                        
            else:
                break
        print("RecebidoCompleto: ", resp)
        return resp
        
    
    # -------------------------------------------------------------------------------------------------
    def Checksum(self, msg): #O parâmetro deve ser uma string
        data = bytearray(msg.encode("utf-8"))
        
        # Inicialize o checksum com 0.
        checksum = 0

        # Loop através de cada par de bytes na sequência de dados.
        for i in range(0, len(data), 2):
            # Combine dois bytes em uma palavra de 16 bits.
            word = (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
            
            # Adicione a palavra ao checksum.
            checksum += word
            
            # Verifique se houve um carry-out e ajuste o checksum, se necessário.
            if checksum > 0xFFFF:
                checksum = (checksum & 0xFFFF) + 1

        # Faça o complemento de um para obter o checksum de 16 bits.
        checksum = ~checksum & 0xFFFF #Checksum string
        print(hex(checksum))
        
        #Converte os pares dos caracteres hexa do checksum em caracteres ASCII
        checksum_final = chr(int(format(checksum, '04x')[:2],16)) + chr(int(format(checksum, '04x')[2:5],16))
        return checksum_final

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
        mensagem = mensagem.replace('!', '!!')
        for i in range(len(_bytes)):
           mensagem = mensagem.replace(_bytes[i], '!' + _bytes[i])
        return mensagem
    
    # -------------------------------------------------------------------------------------------------
    def RetirarByteStuffing(self, mensagem, _bytes):
        mensagem = mensagem.replace('!!', '!')
        for i in range(len(_bytes)):
            mensagem = mensagem.replace('!' + _bytes[i], _bytes[i])
        return mensagem
    
    # -------------------------------------------------------------------------------------------------
    #Todas os parâmetros vão estar corretos e e como string
    def EncapsulamentoQuadro(self, mensagem, controle, NumeroPacote, cksum_quadro):
        quadro = '[' + controle + NumeroPacote +  mensagem + str(cksum_quadro) + ']'
        return quadro

    def DesencapsulaQuadro(self, quadro):
        quadro_recuperado = quadro.replace(self.Bytes_Bytestuffing,"")
        return quadro_recuperado
    
    def SeparaMensagem(self, Mensagem, nbytes):
        BytesMensagem = bytes(Mensagem, 'utf-8')
        Blocos = []
        bloco = []
        
        for i in range(0, len(BytesMensagem), nbytes):
            bloco = BytesMensagem[i:i + nbytes]
            Blocos.append(bloco)
        
        return Blocos
    
    def VerificaIntegridadeQuadro(self, quadro):
        stringQuadro = quadro.decode('utf-8')
        if len(stringQuadro) > 0:
            print(stringQuadro[0])
            print(stringQuadro[len(stringQuadro) -1])
            if stringQuadro[0] == '[' and stringQuadro[len(stringQuadro) -1] == ']':
                if(stringQuadro[1] == 'D' or stringQuadro[1] == 'C'):
                    print('Quadro Verificado')
                else:
                    print('Falta o D ou C')
            else:
                print('O quadro nao comeca com [ ou nao termina com ')
        else:
            print('quadro vazio')
    
    def separaTamanho(self, msg, tamanho):  
        blocos = [msg[i:i+tamanho] for i in range(0, len(msg), tamanho)]
        return blocos