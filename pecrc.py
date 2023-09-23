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

import sys
import canal_tp1

class PECRC:
  
    
    NumeroQuadroEnvia = '0'
    NumeroControleAnterior = bytes('1', 'utf-8')
    
    # testeCkS = '00'
    
    def __init__(self, port, host='' ):
        self.link = canal_tp1.Link(port,host)

    def close(self):
        self.link.close()
        
####################################################################
# A princípio, só é preciso alterar as duas funções a seguir.
  
    # -------------------------------------------------------------------------------------------------
    def send(self,message):
        quadro = bytearray()
        
        quadro.append(ord('D'))
        quadro.append(ord(self.NumeroQuadroEnvia))
        quadro.append(0)
        quadro.append(0)
        
        
        for i in range(0, len(message)):
            quadro.append(message[i])
        
        chks = self.Checksum(quadro[4:])
        quadro = self.ColocarByteStuffing(quadro)
        
        quadro[2] = chks[0]
        quadro[3] = chks[1]
        
        self.link.send(bytes('[', 'utf-8'))
        self.link.send(quadro)
        # self.link.send(bytes(']', 'utf-8'))
        
        # print("Quadro: ", quadro)
        
        for i in range(0, 4):
            try:
                frame = self.link.recv(1500)
                
                if(len(frame) == 6):
                    if(self.NumeroQuadroEnvia == '0'):
                        if(frame[0] == ord('[') and 
                           frame[1] == ord('C') and 
                           frame[2] == ord(self.NumeroQuadroEnvia) and
                           frame[3] == 140 and
                           frame[4] == 159 and
                           frame[5] == ord(']') 
                            ):
                            
                            if(self.NumeroQuadroEnvia == '0'):
                                self.NumeroQuadroEnvia = '1'
                            else:
                                self.NumeroQuadroEnvia = '0'
                        else:
                            raise
                    else:
                        if(frame[0] == ord('[') and 
                            frame[1] == ord('C') and 
                            frame[2] == ord(self.NumeroQuadroEnvia) and
                            frame[3] == 140 and
                            frame[4] == 158 and
                            frame[5] == ord(']') 
                            ):
                            
                            if(self.NumeroQuadroEnvia == '0'):
                                self.NumeroQuadroEnvia = '1'
                            else:
                                self.NumeroQuadroEnvia = '0'
                            
                        else:
                            raise
                else:
                    raise
                                
                return
            except:
                self.link.send(bytes('[', 'utf-8'))
                self.link.send(quadro)
                self.link.send(bytes(']', 'utf-8'))
                
        print('Deu tudo errado')
        sys.exit()
        
                


    def recv(self):
        received = bytes()
        quadoNovoEncontrado = False
        Times = 0
        
        while(True):
            
            DouC = bytes()
            Controle = bytes()
            Chks = bytes()
            byteRecebido = bytes()
            QuadroRecebidoCorretamente = False
            
            if(quadoNovoEncontrado == False):
                byteRecebido = self.link.recv(1)
                
            if(byteRecebido == bytes('', 'utf-8') and Times == 0):
                break
            Times +=1
            if(byteRecebido == bytes('[', 'utf-8') or quadoNovoEncontrado == True):
                DouC += self.link.recv(1)
                Controle += self.link.recv(1)
                Chks += self.link.recv(2)
                
                erroEnquadramento = False
                while(True):
                    try:
                        byteRecebido = self.link.recv(1)
                        
                        if(byteRecebido == bytes('!', 'utf-8')):
                            byteRecebido = self.link.recv(1)
                            received += byteRecebido
                        else:
                            if(byteRecebido == bytes(']', 'utf-8')):
                                break
                            else:
                                received += byteRecebido
                                
                        if(len(received) > 1500):
                            # print('Erro de Enquadramento')
                            received = bytes()
                            erroEnquadramento = True
                            break
                    except:
                        # print('Demorou d+')
                        break
                
                if(erroEnquadramento):
                    quadoNovoEncontrado = self.ProcuraInicioNovoQuadro()
                    continue
            
            verificacao_checksum = self.VerificaChecksum(received, Chks)
            verificacao_controle = Controle != self.NumeroControleAnterior
            if(DouC == bytes('D', 'utf-8') and verificacao_checksum and verificacao_controle):
                QuadroRecebidoCorretamente = True
                self.NumeroControleAnterior = Controle
                        
            
            if(QuadroRecebidoCorretamente):
                ACK = bytearray()
                
                ACK.append(ord('['))
                ACK.append(ord('C'))
                ACK.append(ord(Controle))
                # print('Controle: ', Controle)
                
                if(Controle == bytes('0', 'utf-8')):
                    ACK.append(140)
                    ACK.append(159)
                else:
                    ACK.append(140)
                    ACK.append(158)
                    
                ACK.append(ord(']'))
                self.link.send(ACK)
                break
            else:
                received = bytes()
                   
        # print('Mensagem Recebida: ', received)
        return received
        
        
    # -------------------------------------------------------------------------------------------------
    def Checksum(self, msg):
        
        data = msg
        
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
        checksum = ~checksum & 0xFFFF
        # print("checksum",checksum)
        # print(hex(checksum))
        
        byte1 = (checksum >> 8) & 0xFF
        byte2 = checksum & 0xFF
        # print("b1:",byte1)
        # print("b2:",byte2)
        
        # print(int(hex(byte1),16))
        
        chk_16bits = [byte1,byte2]
        # print("chk_16bits:",chk_16bits)
        
        return chk_16bits
    # -------------------------------------------------------------------------------------------------
    def ColocarByteStuffing(self, mensagem):
        msg = bytearray()
        for i in range(0, len(mensagem)):
            if(mensagem[i] == ord(']') or mensagem[i] == ord('[') or mensagem[i] == ord('!')):
                msg.append(ord('!'))
                msg.append(mensagem[i])
            else:
                msg.append(mensagem[i])
        return msg
    
        
    def VerificaChecksum(self, Quadro, chks):
        if(self.Checksum(Quadro)[0] == chks[0] and self.Checksum(Quadro)[1] == chks[1]):
            return True
        else:
            return False
    
    def ProcuraInicioNovoQuadro(self):        
        atual = bytes()
        anterior = bytes()
        
        while(True):
            atual = self.link.recv(1)
            if(atual == bytes('[', 'utf-8') and anterior == bytes(']', 'utf-8')):
                print('Achei')
                break
            else:
                anterior = atual
        return True
        