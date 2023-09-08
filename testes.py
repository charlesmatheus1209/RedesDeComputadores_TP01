class pecrc1:
    contador = 0
    mensagem = bytes()
    def send(self, mensagem):
        # print(mensagem)
        numeroChecksum = self.calcChecksum(mensagem)
        checksum = hex(numeroChecksum)[2:6]
        
        # print(bytes(checksum, 'utf-8'))
        
        # Montagemdo quadro
        quadro = list()

        quadro.append(bytes('[', 'utf-8'))
        quadro.append(bytes('D', 'utf-8'))
        quadro.append(bytes('0', 'utf-8'))
        quadro.append(mensagem)
        quadro.append(bytes(checksum,'utf-8'))
        quadro.append(bytes(']', 'utf-8'))
        
        quadroEnviar = b''.join(quadro)
        
        return quadroEnviar
        
    def calcChecksum(self, mensagem):
        numero = 100000
        # print(numero % 65536)
        return 60000
    
    def decodificar(self, mensagem):
        print('nao feita')
        
    def getValor(self):
        byte = bytes()
        byte = self.mensagem[self.contador]
        self.contador += 1
        return byte.to_bytes(1)

p = pecrc1()

# mensagem
mensagemcodificada = "mensagem0000![!]"
bytesmessage = mensagemcodificada.encode()

# função enviar
texto = p.send(bytesmessage)
p.mensagem = texto
print(p.mensagem)

MENSAAGEMFINAL = bytes()
while True:
    byteRecebido = p.getValor()
    if(byteRecebido == bytes('[', 'utf-8')):
        # print(byteRecebido)
        DouC = p.getValor()
        Controle = p.getValor()
        while True:
            byteRecebido = p.getValor()
            if(byteRecebido == bytes('!', 'utf-8')):
                byteRecebido = p.getValor()
                continue
            print(byteRecebido)
            MENSAAGEMFINAL += byteRecebido
            if(byteRecebido == bytes(']', 'utf-8')):
                break
        break

check = MENSAAGEMFINAL[(len(MENSAAGEMFINAL)-5):(len(MENSAAGEMFINAL)-1)]
intChecksum = int(check,16)
print(MENSAAGEMFINAL[0:(len(MENSAAGEMFINAL)-1)])
print(int(check,16))

print(intChecksum == p.calcChecksum(MENSAAGEMFINAL))