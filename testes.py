def separaTamanho(msg, tamanho):  
    blocos = [msg[i:i+tamanho] for i in range(0, len(msg), tamanho)]
    return blocos
        
    
str = "abcdefg"

print(separaTamanho(str, 5))
