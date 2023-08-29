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

#Todas os parâmetros vão estar corretos e e como string
def EncapsulamentoQuadro(mensagem,controle,pacote,cksum_quadro):
    separador ="$%#$%#"
    quadro = ""
    quadro = '[' + controle + separador + pacote + separador + mensagem + separador + str(cksum_quadro) + ']'
    return quadro

def RetiraSeparador(quadro):
    quadro_recuperado = quadro.split("$%#$%#")
    return quadro_recuperado

def DesencapsulaQuadro(quadro):
    sMarcador = quadro[3:-1]
    lista = sMarcador.split("$%#$%#")
    return lista




# Checksum('Arroz')

# print(VerificaChecksum('Arroz', Checksum('Arroz')))
# print("Hello World")

print(DesencapsulaQuadro("b.[D$%#$%#1$%#$%#b'Conteudo '$%#$%#211]"))
# print(DesencapsulaQuadro(EncapsulamentoQuadro("OIMUNDO","D","3","265")))

