# Search Engine Natural Language Grammar (BNF)

Este projeto demonstra como implementar e validar uma gramática formal (BNF) para perguntas e respostas de um usuário a um search engine, utilizando Python.

## 📄 Arquivos principais

- **DefinicaoGramatical.py**  
  Implementa a lógica de validação de sentenças em linguagem natural segundo a gramática BNF definida, reconhecendo perguntas e respostas do usuário e sugerindo respostas automáticas para perguntas.

- **AnalisadorLexico.py**  
  Responsável pela análise léxica das sentenças, separando tokens, validando caracteres e palavras, e auxiliando na identificação dos elementos da linguagem.

---

## 🧩 Gramática BNF utilizada

A gramática está baseada em perguntas e respostas naturais sobre documentos.  
Exemplo de definição (veja o arquivo `GramaticalBNF.txt`):

```
<sentenca> ::= <pergunta> | <resposta>

<pergunta> ::= "Qual documento está no" <formato> "?"
             ; resposta: "O formato é" <formato> "."
             | "Qual tamanho tem" <formato> "?"
             ; resposta: "Quero tamanho maior que" <numero> "."
             | "Qual documento tem" <titulo> "?"
             ; resposta: "O título é" <titulo> "."
             | "Quais documentos estão entre" <data> "e" <data> "?"
             ; resposta: "O documento foi criado em" <data> "."
             | "Existe documento com" <palavra_chave> "?"
             ; resposta: "Prefiro documentos com" <palavra_chave> "."
             | "Mostre documentos do tipo" <formato> "com tamanho maior que" <numero> "?"
             ; resposta: "O formato é" <formato> ". Quero tamanho maior que" <numero> "."

<resposta> ::= "O formato é" <formato> "."
             | "Quero tamanho maior que" <numero> "."
             | "O título é" <titulo> "."
             | "O documento está em" <formato> "."
             | "O documento foi criado em" <data> "."
             | "Prefiro documentos com" <palavra_chave> "."
```

---

## 🛠️ Como funciona

- O usuário digita uma sentença (pergunta ou resposta).
- O analisador léxico (`AnalisadorLexico.py`) separa os tokens e valida a entrada.
- O analisador sintático (`DefinicaoGramatical.py`) verifica se a sentença corresponde a alguma regra da gramática BNF.
- Se for uma pergunta, o sistema sugere uma resposta padrão conforme a gramática.
- Se for uma resposta, apenas valida a estrutura.

---

## 💬 Exemplos de uso

### Perguntas válidas:
- `Qual documento está no PDF?`
- `Qual tamanho tem DOCX?`
- `Qual documento tem Relatorio Final?`
- `Quais documentos estão entre 01/01/2023 e 31/12/2023?`
- `Existe documento com orçamento anual?`
- `Mostre documentos do tipo TXT com tamanho maior que 1000?`

### Respostas válidas:
- `O formato é PDF.`
- `Quero tamanho maior que 1000.`
- `O título é Relatorio Final.`
- `O documento está em DOCX.`
- `O documento foi criado em 01/01/2023.`
- `Prefiro documentos com orçamento anual.`

---

## 📚 Foco gramatical

O objetivo principal é mostrar como uma gramática BNF pode ser aplicada para reconhecer e validar sentenças em linguagem natural, permitindo a construção de sistemas de busca mais inteligentes e adaptados ao usuário.

---

## 🚀 Como executar

1. Certifique-se de ter Python 3 instalado.
2. Execute o arquivo `DefinicaoGramatical.py`:
   ```
   python DefinicaoGramatical.py
   ```
3. Digite perguntas ou respostas conforme os exemplos acima para testar a validação gramatical.

---

## 📁 Estrutura recomendada

```
Atividade 2 - 25pt - Python/
│
├── DefinicaoGramatical.py
├── AnalisadorLexico.py
├── GramaticalBNF.txt
└── README.md
```

---

## ✍️ Observação

O foco deste projeto é didático, para estudo de gramáticas formais e análise sintática em linguagem natural.