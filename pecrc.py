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
        # Aqui, PPSRT deve fazer:
        #   - fazer o encapsulamento de cada mensagem em um quadro,
        #   - calcular o Checksum do quadro e incluído,
        #   - fazer o byte stuffing durante o envio da mensagem,
        #   - aguardar pela mensagem de confirmação,
        #   - retransmitir a mensagem se a confirmação não chegar.
        #        Para controlar a retransmissão, use algo como:
        #        try:
        #            frame = self.link.recv(1500)
        #        except TimeoutError: # use para tratar temporizações
        #            print("Timeout") # cuidaria da retransmissão
        #        return frame
        #
        
        MsgComByteStuffing = self.ColocarByteStuffing(message.decode(), self.Bytes_Bytestuffing)
        Checksum = hex(self.Checksum(MsgComByteStuffing))[2:6]
        
        quadro = list()

        quadro.append(bytes('[', 'utf-8'))
        quadro.append(bytes('D', 'utf-8'))
        quadro.append(bytes('0', 'utf-8'))
        quadro.append(bytes(MsgComByteStuffing, 'utf-8'))
        quadro.append(bytes(Checksum,'utf-8'))
        quadro.append(bytes(']', 'utf-8'))
        print(quadro)
        quadroEnviar = b''.join(quadro)
        
        print(quadroEnviar)
        
        self.link.send(quadroEnviar)

    def recv(self):
        MENSAAGEMFINAL = bytes()
        resp = bytes()
        recebidoCompleto = False
        while True:
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
                break
        if(recebidoCompleto == True):
            checkRecebido = MENSAAGEMFINAL[(len(MENSAAGEMFINAL)-5):(len(MENSAAGEMFINAL)-1)]
            intChecksum = int(checkRecebido,16)
            MensagemRecebida = MENSAAGEMFINAL[0:(len(MENSAAGEMFINAL)-5)]
            print("Mensagem recebida: ", (MensagemRecebida))
            resp = MensagemRecebida
            
        print("RecebisoCompleto: ", recebidoCompleto)
        return resp
        
    
    # -------------------------------------------------------------------------------------------------
    def Checksum(self, data1):
            # Inicialize o checksum com 0.
        data = bytes(data1, 'utf-8')
        checksum = 0

        # Loop através de cada par de bytes na sequência.
        for i in range(0, len(data), 2):
            # Combine os dois bytes em um número de 16 bits.
            # Se houver um byte ímpar no final, adicione 0x00 como o byte inferior.
            byte1 = data[i]
            byte2 = data[i + 1] if i + 1 < len(data) else 0x00
            combined_byte = (byte1 << 8) + byte2

            # Adicione o valor combinado ao checksum.
            checksum += combined_byte

            # Verifique se houve um estouro de 16 bits (carry).
            if checksum > 0xFFFF:
                # Se houver, ajuste o checksum.
                checksum = (checksum & 0xFFFF) + 1

        # O resultado é o complemento de um do checksum final de 16 bits.
        checksum = 0xFFFF - checksum

        return checksum

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
                