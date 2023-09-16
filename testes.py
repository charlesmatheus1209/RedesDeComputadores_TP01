# --------------------------------Cálculo Checksum------------------------------- #
def Checksum(msg): #O parâmetro deve ser uma string
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

chk = Checksum("olafola")
# print(hex(chk))
# print(int(chk))
print(chk)

# "Oi aigo !!" = 0x968c
# "Oi" = 0xb096
# "Marielle" = 0x6e63

# --------------------------------Colocar Stuffing-------------------------------- #
def ColocarByteStuffing(mensagem, _bytes):
        mensagem = mensagem.replace('!', '!!')
        for i in range(len(_bytes)):
           mensagem = mensagem.replace(_bytes[i], '!' + _bytes[i])
        return mensagem

    
# Bytes_Bytestuffing = '[]'
# msg_stuf = ColocarByteStuffing("[Bom dia!Mund[oC]omo! Ser]",Bytes_Bytestuffing)
# msg_stuf2 = ColocarByteStuffing("[Bom dia!!Mundo omo! Se !!!r]",Bytes_Bytestuffing)
# #![Bom dia!!!!Mundo omo!! Se !!!!!!r!]
# #print(msg_stuf)
# print("![Bom dia!!!!Mundo omo!! Se !!!!!!r!]")
# print(msg_stuf2)

# --------------------------------Retirada Stuffing-------------------------------- #
def RetirarByteStuffing(mensagem, _bytes):
        mensagem = mensagem.replace('!!', '!')
        for i in range(len(_bytes)):
            mensagem = mensagem.replace('!' + _bytes[i], _bytes[i])
        return mensagem

#print(RetirarByteStuffing(msg_stuf,Bytes_Bytestuffing))
# print(RetirarByteStuffing(msg_stuf2,Bytes_Bytestuffing))
# print("[Bom dia!!Mundo omo! Se !!!r]")




# ---------------------Testes ------------------------------#
 # print("Codigo ascii dec: ", ord(Checksum[0:1]))
            # # print("pc", chr(ord(Checksum[0:1])))
            # # print("sc", chr(ord(Checksum[1:2])))
            # # print(bytes(chr(ord(Checksum[0:1])), 'utf-8'))
            # # print(bytes(chr(ord(Checksum[1:2])), 'utf-8'))
            # # print(chr(ord(Checksum[1:2])).encode('utf-8'))
            # # segundo_caractere = bytes(ord(Checksum[1:2]),'utf-8')

            # quadro.append(bytes('[', 'utf-8'))
            # quadro.append(bytes('D', 'utf-8'))
            # quadro.append(bytes(NumeroDoQuadro, 'utf-8'))
            # quadro.append(bytes(bloco, 'utf-8'))
            # quadro.append(bytes(str(Checksum),'utf-8'))
            # # quadro.append(primeiro_caractere)
            # # quadro.append(segundo_caractere)
            # quadro.append(bytes(']', 'utf-8'))