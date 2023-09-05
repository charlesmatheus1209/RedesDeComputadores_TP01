-------------
## Dúvidas
- [ ] Formato e conteúdo da mensagem de onfirmação!
-------------
## Tarefas de implementação
- [ ] Compreensão do enunciado
- [ ] Implementação
    - [ ] Algoritmo checksum
	- [ ] Retirar a impressão de mensagens de depuração
	- [ ] Revisar se os comentários estão adequados 
	- [ ] Inserir como comentário o nome da dupla (início do arquivo)
- [ ] Testes
    - [ ] Roteiro de testes
-------------

## PECRC, um protocolo de enlace confiável

Protocolo implementado em Python, que garante que os dados sejam transmitidos de forma confiável, o que envolve a confirmação da recepção dos dados e a retransmissão de dados perdidos ou corrompidos.

-------------

### Conceitos
#### Enquadramento por Byte-Stuffing
 O enquadramento é a técnica usada para separar os quadros de dados em uma sequência de bits transmitida. No caso do "byte-stuffing", os quadros são delimitados por bytes especiais que não ocorrem normalmente nos dados transmitidos. Se o byte especial aparecer nos dados, ele é "escapado" ou "estufado" com um byte especial adicional para que o receptor saiba que esse é um byte de delimitação de quadro e não parte dos dados reais. Dessa forma, o sistema de comunicação garante a entrega confiável dos dados e também fornece uma maneira de identificar o início e o fim de cada quadro de dados, mesmo que os bytes de delimitação ocorram nos próprios dados.
 
 #### Checksum
 Técnica utilizada para verificar a integridade dos dados durante a transmissão. Seu objetivo é detectar erros de transmissão, como perda ou corrupção de dados, de forma a garantir que os dados recebidos sejam idênticos aos dados transmitidos.
 
 *Funcionamento:*
 
 1.** Geração do Checksum: ** Antes de enviar os dados, o remetente aplica um algoritmo matemático aos dados. Esse algoritmo calcula um valor numérico com base nos dados originais, e esse valor é conhecido como o checksum.
 2.** Transmissão dos Dados e do Checksum: ** Tanto os dados originais quanto o checksum são enviados ao destinatário.
 3.** Verificação do Checksum:** No destinatário, os dados recebidos são submetidos ao mesmo algoritmo de checksum que o remetente usou. O destinatário calcula seu próprio checksum a partir dos dados recebidos.
 4.** Comparação dos Checksums: ** O destinatário compara o checksum calculado a partir dos dados recebidos com o checksum que acompanha os dados. Se os dois checksums forem iguais, isso indica que os dados não foram corrompidos durante a transmissão e que a integridade dos dados foi mantida. Caso contrário, se os checksums forem diferentes, isso indica que ocorreu algum tipo de erro de transmissão.
 
 O checksum é uma técnica eficaz para detectar erros de transmissão, mas não é capaz de corrigi-los. Se um erro for detectado, a ação apropriada geralmente envolve a solicitação de retransmissão dos dados ao remetente para garantir a integridade dos dados.

-------------

### Princípios de operação
O protocolo apresenta as seguintes funcionalidades:

- Enquadramento por byte stuffing;
- Checksum de 16 bits;
- Mensagem de confirmação (ACK) enviado para cada quadro recebido corretamente
- Retransmissão por temporização de 5 segundos

-------------

### Especificação do protocolo
O protocolo utiliza utiliza um quadro com os seguintes campos:

- um marcador de início de quadro que será o caractere '[' (abre-cholchete);
- um caractere de controle que indica se o quadro contém dados ('D') ou confirmação ('C');
- um caractere para numeração dos pacotes, poderá ser '0' ou '1' (note que não um byte com valor 0 ou 1);
- um campo de dados de tamanho variável, com no máximo 1500 bytes;
- um campo de checksum com dois bytes (algoritmo de checksum de 16 bits da internet);
- um marcador de fim de quadro, que será o caractere ']' (fecha-colchete).

|*Descrição*| Marcador  | Controle  | N° pacote  |Dados   | Checksum  |  Marcador |
| :------------:| :------------: | :------------: | :------------: | :------------: | :------------: | :------------: |
|***Conteúdo***|  [ |  D/C |0,1,2,3...   | Máx. 1,5 KB  |16 bits   | ]  |
|***Exemplo***|  [ |  D |  0 | "Olá Mundo"  |  256 |  ] |

Byte stuffing feito usando um ponto de exclamação (!) como caractere de escape. Apenas os caracteres de início de bloco, fim de bloco e o próprio ponto de exclamação, caso ocorram entre os marcadores de início e fim do bloco, precisam ser precedidos do caractere de escape. Qualquer byte encontrado depois de um byte de escape deve ser simplesmente tratados como um byte normal, sem significado especial.

Um ACK deve sempre carregar no campo de numeração o número do quadro que está sendo confirmado.
A única saída esperada a criação do arquivo recebido por recebe.py, com o nome indicado como parâmetro.

-------------

### Sobre a execução dos programas
Devido ao uso de TCP na criação dos links, o programa recebe.py deve sempre ser executado primeiro, pois ele executa a abertura passiva do canal.

-------------

### Links
[Repositório Git Hub](http://localhost/ "link title")

-------------

### Códigos Auxiliares 

#### canal_tp1.py
Camada que encapsula a interface de sockets (pense nele como uma camada física).

```python
import socket

class Link:
  
    def __init__(self, port = 0, host = '' ):
        if host == '':
            orig = (host, int(port))
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.bind(orig)
            listen_socket.listen(1)
            self.tcp_socket, client = listen_socket.accept()
        else:
            dest = (host,int(port))
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.settimeout(5) # usando 5 segundos
            self.tcp_socket.connect(dest)
  
    def send(self,message):
        self.tcp_socket.send(message)

    def recv(self,nbytes):
        try: # essa estrutura repassa temporizações para PPPSRT
            some_bytes = self.tcp_socket.recv(nbytes)
        except socket.timeout:
            raise TimeoutError
        return some_bytes

    def close(self):
        self.tcp_socket.close()
```
#### envia.py
Lê um arquivo e usa o PECRC para enviá-lo através do enlace.

```python
import pecrc  
import os,sys

if len(sys.argv) != 4:
    print('Argumentos: ', sys.argv[0],' arquivo host porto')
    exit()

nome_arquivo = sys.argv[1]
host    = sys.argv[2]
port    = sys.argv[3]

pecrc = pecrc.PECRC( port, host )

arquivo = open(nome_arquivo,'rb')

while True:
    bloco = arquivo.read(1000)  # esse tamanho poderia mudar a cada chamada
    if not bloco: break
    pecrc.send(bloco)

pecrc.close()
arquivo.close()
```
#### recebe.py
Usa o PECRC para receber um arquivo do enlace e salvá-lo no disco.

```python
import pecrc 
import os,sys

if len(sys.argv) != 3:
    print('Argumentos: ', sys.argv[0],' arquivo porto')
    exit()

nome_arquivo = sys.argv[1]
port    = sys.argv[2]


pecrc = pecrc.PECRC( port )

arquivo = open(nome_arquivo,'wb')

while True:
    bloco = pecrc.recv()  # esse tamanho poderia mudar a cada chamada
    if not bloco: break
    arquivo.write(bloco)

pecrc.close()
arquivo.close()
```
