def Checksum(msg):
        
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
str = "abcdefg"

print(Checksum(b'C100'))



