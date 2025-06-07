# 📄 Analisador Sintático em Python

Este projeto é um **interpretador simples de linguagem natural**, com o objetivo de entender comandos do usuário relacionados a arquivos. Ele é composto por dois módulos principais:

- `AnalisadorLexico.py`: identifica os **tokens** e **símbolos** presentes na frase.
- `AnalisadorSintatico.py`: reconhece **estruturas gramaticais**, interpreta **comandos** ou **perguntas**, e retorna uma resposta apropriada.

---

## ⚙️ Como funciona

### 1. Análise Léxica
O analisador léxico divide a frase em palavras e identifica a **categoria gramatical** de cada uma, como:
- `verbo_demostrar`: ações como "mostre", "existe"
- `entidade`: "documento", "arquivo", etc.
- `atributo`: "tamanho", "tipo", etc.
- `tipo`: extensões de arquivo, como "pdf", "mp3"
- `interrogativo`: "qual", "quais"
- `verbo_adicao` : "adicionar", "inclua", etc.
- `identificador`: qualquer palavra fora do vocabulário conhecido

Essas categorias são salvas na **tabela de funcao**.

### 2. Análise Sintática
O analisador sintático tenta casar a estrutura da frase com **regras gramaticais**, por exemplo:

```bnf
<pergunta> ::= <interrogativo> <entidade>
             | <interrogativo> <atributo>
             | <verbo_demonstrar> <entidade> <atributo> <atributo>
             | <verbo_demonstrar> <entidade>

<comando> ::= <verbo_adicao> <entidade> <identificador>
```

Se a estrutura da frase corresponder a uma dessas regras, uma **resposta é gerada** com base em arquivos fictícios no código.

---

## ▶️ Como rodar

1. Execute o programa principal (exemplo):
```bash
python main.py
```

---

## 💬 Exemplos de uso

Digite frases como:

| Frase                                  | Interpretação                                 |
|----------------------------------------|-----------------------------------------------|
| `Qual documento está no "<formato/titulo>"?`                      | Pergunta se existe algum documento            |
| `Qual tipo pdf?`                       | Retorna arquivos com tipo PDF                 |
| `Mostre documento tipo <formato>?`        | Lista documentos com tipo e tamanho           |
| `Existe documento <titulo>?`                     | Verifica se o documento existe                |
| `Mostre documento pdf projeto`         | Busca por um arquivo chamado "projeto.pdf"    |
| `Qual tamanho mp3?`                    | Mostra o tamanho de arquivos mp3              |
| `Adicione o documento com nome Batata tamanho 1200`                    | Adiciona o documento e seu tamanho              |
| `Batata?`                              | ❌ Comando inválido → Mensagem: "Não entendi" |

---

## 📁 Arquivos simulados

O sistema contém uma lista de arquivos de exemplo, como:
- `relatorio.pdf`
- `musica.mp3`
- `video.mp4`
- `projeto.rar`

E cada arquivo tem um **tamanho simulado** para permitir perguntas como:
- `Qual tamanho zip?`
- `Mostre documento mp4?`

---