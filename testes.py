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
    checksum = ~checksum & 0xFFFF
    print("checksum",checksum)
    print(hex(checksum))
    
    byte1 = (checksum >> 8) & 0xFF
    byte2 = checksum & 0xFF
    print("b1:",byte1)
    print("b2:",byte2)
    
    # print(int(hex(byte1),16))
    
    chk_16bits = bytes([byte1,byte2])
    print("chk_16bits:",chk_16bits)
    
    # return 'AB'
    return chk_16bits

chk = Checksum("D0aloMundoBomdia")
# print(hex(chk))
# print(int(chk))
# print(chk)

# import sys

# # Sua variável
# minha_variavel = 42  # Substitua pelo seu valor

# # Obtenha o tamanho em bytes
# tamanho_em_bytes = sys.getsizeof(minha_variavel)

# # Converta para tamanho em bits
# tamanho_em_bits = tamanho_em_bytes * 8

# # Imprima o tamanho em bits
# print("tamanho em bytes:", tamanho_em_bytes)
# print("Tamanho em bits:", tamanho_em_bits)

# hexadecimal = 0x21AB

# # Extraia os bytes de 16 bits individualmente
# byte1 = (hexadecimal >> 8) & 0xFF  # Byte mais significativo
# byte2 = hexadecimal & 0xFF  # Byte menos significativo

# # Imprima os valores de byte1 e byte2
# print("byte1:", byte1)
# print("byte2:", byte2)

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