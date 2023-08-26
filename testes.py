def Checksum(informacao):
        checksum = 0
        
        # Abaixo está a lógica do Checksum. Caso deseje alterá-la basta mudar a seção de código abaixo
        
        for i in range(len(informacao)):
            checksum += i * ord(informacao[i])
        
        # print('A checksum da informação \n{\n' + informacao + '\n}\neh:' + str(checksum) )
        return checksum

def VerificaChecksum(informacao, ValorChecksum):
    checksum = Checksum(informacao)
        
    if(ValorChecksum == checksum):
        # print('A informação chegou perfeitamente')
        return True
    else:
        # print('A informação não chegou perfeitamente')
        return False

# Checksum('Arroz')

print(VerificaChecksum('Arroz', Checksum('Arroz')))
print("Hello World")

