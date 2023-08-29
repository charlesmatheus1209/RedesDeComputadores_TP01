def Checksum(informacao):
        checksum = 0
        
        # Abaixo está a lógica do Checksum. Caso deseje alterá-la basta mudar a seção de código abaixo
        
        for i in range(len(informacao)):
            checksum += i * ord(informacao[i])
        
        # print('A checksum da informação \n{\n' + informacao + '\n}\neh:' + str(checksum) )
        return checksum % pow(2,16)

def VerificaChecksum(informacao, ValorChecksum):
    checksum = Checksum(informacao)
        
    if(ValorChecksum == checksum):
        # print('A informação chegou perfeitamente')
        return True
    else:
        # print('A informação não chegou perfeitamente')
        return False

def ColocarByteStuffing(mensagem, _bytes):
    
    for i in range(len(_bytes)):
        mensagem = mensagem.replace(str(_bytes[i]), '/' + str(_bytes[i]))
    return mensagem

def RetirarByteStuffing(mensagem, _bytes):
    
    for i in range(len(_bytes)):
        mensagem = mensagem.replace('/' + str(_bytes[i]), str(_bytes[i]))
    return mensagem

# Checksum('Arroz')
# print(VerificaChecksum('Arroz', Checksum('Arroz')))

tt = 'aaa#$aaa'
tt = "D$%#$%#1$%#$%#b'Conteudo '$%#$%#211"

resp = tt.split("$%#$%#")

for r in resp:
    print(r)
    
    b"[D$%#$%#1$%#$%#b'Conteudo '$%#$%#211]"