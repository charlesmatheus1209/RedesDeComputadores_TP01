def Checksum(data):
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

    return checksum

chk = Checksum(bytearray("Marielle".encode("utf-8")))
print(hex(chk))

# "Oi aigo !!" = 0x968c
# "Oi" = 0xb096
# "Marielle" = 0x6e63

# Checksum('Arroz')

# print(VerificaChecksum('Arroz', Checksum('Arroz')))
# print("Hello World")

#print(DesencapsulaQuadro("b.[D$%#$%#1$%#$%#b'Conteudo '$%#$%#211]"))
# print(DesencapsulaQuadro(EncapsulamentoQuadro("OIMUNDO","D","3","265")))

