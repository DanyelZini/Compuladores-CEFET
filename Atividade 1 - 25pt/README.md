# Analisador Léxico

Este é um sistema de análise léxica desenvolvido em C++ que processa textos, valida palavras, remove stopwords e gera uma tabela de símbolos. Além disso, permite a interação com um chatbot ou o processamento de arquivos `.txt`.

## Funcionalidades
1. **Validação de caracteres**:
   - Aceita letras (`A-Z`, `a-z`), números (`0-9`), caracteres de pontuação e caracteres especiais do teclado brasileiro.
   - Exibe uma mensagem de erro e encerra o programa ao encontrar caracteres inválidos.

2. **Stopwords**:
   - Remove palavras comuns (stopwords) durante o processamento.
   - A lista de stopwords é carregada de um arquivo externo (`stopwords.txt`).
   - Lista adquirida em https://github.com/stopwords-iso/stopwords-pt/blob/master/stopwords-pt.txt

3. **Tabela de Símbolos**:
   - Armazena palavras únicas que não são stopwords em uma estrutura ordenada.

4. **Fila de Tokens**:
   - Armazena todas as palavras e delimitadores processados para análise posterior.

5. **Similaridade de Palavras**:
   - Corrige palavras com grafia incorreta com base em similaridade (ex.: `exceção`, `excessão`, `excecao`).

6. **Menus Interativos**:
   - Permite interação com um chatbot ou processamento de arquivos `.txt`.

---

## Como Usar o Menu

### 1. Executar o Programa
Compile e execute o programa. O menu principal será exibido.

### 2. Menu Principal
O menu principal apresenta as seguintes opções:


#### Opção 1: ChatBot
- Digite frases diretamente no console.
- O sistema processará as palavras, validará os caracteres.
- Digite `sair` para voltar ao menu principal.

#### Opção 2: Arquivo `.txt`
- Coloque o arquivo `.txt` na pasta `./entrada/`.
- Digite o nome do arquivo (sem a extensão `.txt`) para processá-lo.
- O sistema processará o conteúdo do arquivo.
- Digite `sair` para voltar ao menu principal.

#### Opção 3: Token Fila
- Exibe todos os tokens processados que estão armazenados na fila de tokens.
- Use esta opção para visualizar os tokens gerados durante o processamento.

#### Opção 4: Tabela de Símbolos
- Exibe todas as palavras únicas que não são stopwords e que foram armazenadas na tabela de símbolos.
- Use esta opção para visualizar as palavras processadas e organizadas.


#### Opção 0: Sair
- Encerra o programa.

---

## Saída do Sistema
Os resultados do processamento são salvos na pasta `./saida/` nos seguintes arquivos:
1. **`stopwords-pt.txt`**: Lista de stopwords carregadas.
2. **`tabela-simbolos.txt`**: Palavras únicas que não são stopwords.
3. **`token-fila.txt`**: Tokens gerados durante o processamento.

---

## Requisitos
- Compilador C++ compatível com C++17 ou superior.
- Arquivo `stopwords.txt` na pasta `./entrada/` contendo a lista de stopwords.

---

## Autor
Danyel Martins Zini Silva - 20243014020  
[GitHub Repository](https://github.com/DanyelZini/Compuladores-CEFET)